import pandas as pd
import numpy as np
from dotenv import load_dotenv
from tenable.io import TenableIO

from models.tag import Tag
from models.user import User
from models.exclusion import Exclusion
from models.agent_group import AgentGroup


class SheetNotFound(Exception):
    '''Raised when requested sheet is not in the workbook.'''


model_classes = {
    'users': User,
    'exclusions': Exclusion,
    'tags': Tag,
    'agent_groups': AgentGroup
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

    def build_commands(self, sheet_name: str):
        df = self._work_sheets.get(sheet_name)
        if df is None:
            raise SheetNotFound(f"'{sheet_name}' not found in {self._file_path}")

        # clean DataFrame and convert to list of dicts
        data = df.replace(np.nan, None).to_dict('records')
        
        cls = model_classes.get(sheet_name)
        if cls is None and sheet_name.startswith('tags_') or sheet_name.endswith('_tags'):
            cls = model_classes.get('tags')

        # convert to data model if it exists
        if cls is not None:
            return [cls(**record) for record in data]

    def execute(self, sheet_name: str):
        commands = self.build_commands(sheet_name)
        print(f'executing sheet: {sheet_name}')
        for command in commands:
            print(command.describe)
            command.execute(self._session)

    def get_records(self, sheet_name: str):
        commands = self.build_commands(sheet_name)
        return [command.dict() for command in commands]




# cleanup function for testing
def del_users():
    load_dotenv()
    tio = TenableIO()
    for user in tio.users.list():
        if '+test' in user['username']:
            print(f"deleting: {user['username']}")
            tio.users.delete(user['id'])

# def main():
    # execute('users')
    # execute('exclusions')


# if __name__ == '__main__':
    # main()