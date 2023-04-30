import pandas as pd
import numpy as np
from dotenv import load_dotenv
from typing import Optional
from tenable.io import TenableIO

from models.tag import Tag
from models.user import User
from models.exclusion import Exclusion
from models.agent_group import AgentGroup
from models.network import Network
from models.scanner_group import ScannerGroup

from processors import expand_users_with_groups


class SheetNotFound(Exception):
    '''Raised when requested sheet is not in the workbook.'''


data_models = {
    'agent_groups': AgentGroup,
    'exclusions': Exclusion,
    'networks': Network,
    'scanner_groups': ScannerGroup,
    'tags': Tag,
    'users': User
}


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
            raise "unknown data model"

        return [cls(**record) for record in data]

    def dict(self):
        return [record.dict() for record in self.records]


class Excel:
    def __init__(self, file_path: str) -> None:
        self.excel = pd.ExcelFile(file_path)
        self.work_sheets = {name: WorkSheet(self.excel, name) for name in self.excel.sheet_names}
        self._file_path = file_path
        self.sheet_names = self.excel.sheet_names

    def get_objs(self, sheet_name: str, action=None):
        objs = self.work_sheets[sheet_name].records
        # if sheet_name == 'users':
        #     objs = [obj for obj in expand_users_with_groups(objs)]

        if action is not None:
            for obj in objs:
                obj.action = action
        return objs

    def dict(self):
        return {k: v.dict() for k, v in self.work_sheets.items()}



class WorkSheets:

    def __init__(self, file_path: str, sheet_names: Optional[list[str]]=None) -> None:
        # read worksheets into a dictionary
        xl = pd.ExcelFile(file_path)
        self._work_sheets = {s: xl.parse(s) for s in xl.sheet_names}
        self.sheets = sheet_names
        self._file_path = file_path

    def _load_sheet(self, sheet_name: str):
        df = self._work_sheets.get(sheet_name)
        if df is None:
            raise SheetNotFound(f"'{sheet_name}' not found in {self._file_path}")

        # clean DataFrame and convert to list of dicts
        data = df.replace(np.nan, None).to_dict('records')

        # the name of the sheet determines the data type
        data_type = sheet_name

        # allow for more than one sheet of tags
        if sheet_name.startswith('tags') or sheet_name.endswith('tags'):
            data_type = 'tags'
        
        #  - expecting either a defined sheet name or starting/ending with 'tags'
        cls = data_models.get(sheet_name)
        if cls is None and sheet_name.startswith('tags') or sheet_name.endswith('tags'):
            cls = data_models.get('tags')

        # convert to data model 
        if cls is not None:
            return [cls(**record) for record in data]

    def get_objs(self, sheet_name: str, action=None):
        objs = self._load_sheet(sheet_name)
        if action is not None:
            for obj in objs:
                obj.action = action
        return objs

    def get_records(self, sheet_name: str):
        commands = self._load_sheet(sheet_name)
        return [command.dict() for command in commands]

