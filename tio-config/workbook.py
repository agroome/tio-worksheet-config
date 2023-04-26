import pandas as pd
import numpy as np
from dotenv import load_dotenv
from tenable.io import TenableIO

from models.tag import Tag
from models.user import User
from models.exclusion import Exclusion
from models.agent_group import AgentGroup
from models.network import Network
from models.scanner_group import ScannerGroup


class SheetNotFound(Exception):
    '''Raised when requested sheet is not in the workbook.'''


model_classes = {
    'agent_groups': AgentGroup,
    'exclusions': Exclusion,
    'networks': Network,
    'scanner_groups': ScannerGroup,
    'tags': Tag,
    'users': User
}


class WorkSheets:

    def __init__(self, file_path: str, session: TenableIO = None) -> None:
        # read worksheets into a dictionary
        xl = pd.ExcelFile(file_path)
        self._work_sheets = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}
        self._file_path = file_path

        # prepare a tio session if not passed in
        self._session = session
        if self._session is None: 
            load_dotenv()
            self._session = TenableIO()

    @property
    def sheets(self):
        return list(self._work_sheets)

    def _load_sheet(self, sheet_name: str):
        df = self._work_sheets.get(sheet_name)
        if df is None:
            raise SheetNotFound(f"'{sheet_name}' not found in {self._file_path}")

        # clean DataFrame and convert to list of dicts
        data = df.replace(np.nan, None).to_dict('records')
        
        # select data model based on the name of the sheet
        #  - expecting either a defined sheet name or starting/ending with 'tags'
        cls = model_classes.get(sheet_name)
        if cls is None and sheet_name.startswith('tags') or sheet_name.endswith('tags'):
            cls = model_classes.get('tags')

        # convert to data model 
        if cls is not None:
            return [cls(**record) for record in data]

    def execute(self, sheet_name: str):
        commands = self._load_sheet(sheet_name)
        print(f'executing sheet: {sheet_name}')
        for command in commands:
            print(command.describe)
            command.execute(self._session)

    def get_records(self, sheet_name: str):
        commands = self._load_sheet(sheet_name)
        return [command.dict() for command in commands]


# cleanup function for testing
def del_users():
    load_dotenv()
    tio = TenableIO()
    for user in tio.users.list():
        if '+test' in user['username']:
            print(f"deleting: {user['username']}")
            tio.users.delete(user['id'])
