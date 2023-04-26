import string
import random
import textwrap

from models.base_model import CustomBase
from typing import ClassVar, Optional
from pydantic import Field, validator

PASSWORD_LENGTH = 20

def generate_password(length=PASSWORD_LENGTH):
    special_chars = '`~!@#$%^&*()-_+='
    password_chars = string.digits + string.ascii_letters + special_chars
    return "".join(random.choices(password_chars, k=length))


tio_users = None
def init_tio_users(tio):
    global tio_users
    if tio_users is None:
        tio_users = {user['username']: user for user in tio.users.list()}

class User(CustomBase):
    username: str
    name: Optional[str]
    email: Optional[str]
    permissions: Optional[int] = 64
    groups: Optional[list[str]] = None
    password: Optional[str] = Field(default=generate_password(), repr=False)
    tio_groups: ClassVar = None

    @validator('groups', pre=True)
    def split_string(cls, value):
        if isinstance(value, str):
            value = [v.strip() for v in value.split(',')]
        return value
    
    @property
    def describe(self):
        text = f'''
        creating User(
            username={self.username}")
            email={self.email}")
            name={self.name}")
            permissions={self.permissions}")
            groups={self.groups}")
        )
        '''
        return textwrap.dedent(text)
        
    def execute(self, tio):
        try:
            # load tio groups once as a class variable
            if User.tio_groups is None:
                User.tio_groups = {group['name']: group for group in tio.groups.list()}
        except Exception as e:
            print(f'error: {e.args}')

        try:
            values = self.dict(exclude={'groups'})
            user = tio.users.create(**values)
            if self.group is not None:
                for group_name in self.group.replace(' ', '').split(','):
                    try: 
                        # get group from known groups or create group
                        group = User.tio_groups.get(group_name)
                        if group is None:
                            print(f"creating: Group(name='{group_name}')")
                            group = tio.groups.create(group_name)
                            # update known groups
                            User.tio_groups[group_name] = group

                        print(f'adding {user["username"]} to {group_name}')
                        tio.groups.add_user(group['id'], user['id'])

                    except Exception as e:
                        print(f'error: {e.args}')

        except Exception as e:
            pass