import pandas as pd
import numpy as np
from dotenv import load_dotenv
from typing import Optional
from tenable.io import TenableIO

from command import BatchCommands
from session import data_models

from models.agent_group import AgentGroup
from models.exclusion import Exclusion
from models.group import Group
from models.network import Network
from models.scanner_group import ScannerGroup
from models.tag import Tag
from models.user import User

# from processors import expand_users_with_groups

class SheetNotFound(Exception):
    '''Raised when requested sheet is not in the workbook.'''


class WorkSheet:
    def __init__(self, excel: pd.ExcelFile, name: str) -> None: 
        self.name = name
        self.excel = excel
        self.records = self.parse_records()

    def parse_records(self):
        df = self.excel.parse(self.name)
        data = df.replace(np.nan, None).to_dict('records')

        # the name of the sheet determines the data type
        data_type = self.name
        if data_type.startswith('tags') or data_type.endswith('tags'):
            data_type = 'tags'
        
        cls = data_models.get(data_type)
        if cls is None:
            raise Exception(f"[{data_type}]: unknown data model")

        return [cls(**record) for record in data]

    def dict(self):
        return [record.dict() for record in self.records]


class Excel:
    def __init__(self, file_path: str, sheet_names: Optional[list]=None) -> None:
        self.excel = pd.ExcelFile(file_path)
        self._file_path = file_path
        self.sheet_names = self.excel.sheet_names
        if sheet_names is not None:
            self.sheet_names = [name for name in self.sheet_names if name in sheet_names]
        self.work_sheets = {name: WorkSheet(self.excel, name) for name in self.sheet_names}

    def get_objs(self, sheet_name: str, action):
        objs = self.work_sheets[sheet_name].records
        # if sheet_name == 'users':
        #     objs = [obj for obj in expand_users_with_groups(objs)]
        print(f'get objs for {action}')
        for obj in objs:
            obj.action = action
        return objs

    def execute(self, sheet_names:list = None, action: str ='create', dry_run: bool = False):
        if sheet_names is None:
            sheet_names = self.sheet_names
        for sheet in sheet_names:
            print(f"get batch for {action}")
            cmds = BatchCommands(self.get_objs(sheet, action), action)
            cmds.execute(dry_run)

    def dict(self):
        return {k: v.dict() for k, v in self.work_sheets.items()}

