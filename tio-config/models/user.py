import string
import random
import textwrap

from models.base_model import CustomBase
from collections import defaultdict
from typing import ClassVar, List, Optional
from pydantic import Field, validator
from session import get_cached

PASSWORD_LENGTH = 20

# tio_users = {'user': u for u in get_cached('users')}

def generate_password(length=PASSWORD_LENGTH):
    special_chars = '`~!@#$%^&*()-_+='
    password_chars = string.digits + string.ascii_letters + special_chars
    return "".join(random.choices(password_chars, k=length))


class Group(CustomBase):
    name: str
    api_name: ClassVar = 'groups'

    @property
    def id(self) -> int:
        groups = get_cached('groups')
        group = groups.get(self.name)
        return group['id']


class User(CustomBase):
    username: str
    name: Optional[str]
    email: Optional[str]
    permissions: Optional[int] = 64
    groups: List[Group] = None
    password: Optional[str] = Field(default=generate_password(), repr=False)
    api_name: ClassVar = 'users'

    @validator('username')
    def to_lower(cls, value):
        if isinstance(value, str):
            value = value.lower()
        return value


    @validator('groups', pre=True)
    def split_string(cls, value):
        if isinstance(value, str):
            value = [dict(name=group_name) for group_name in value.split(',')]
        elif isinstance(value, list):
            value = [dict(name=group_name) for group_name in value]
        return value
    
    @property
    def id(self):
        tio_users = get_cached('users')
        user = tio_users.get(self.username)
        if user is None:
            raise IndexError(f'[{self.username}]: not found')
        return user['id']

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
        

def process_users(objects, action='create'):
    tio_groups = get_cached('groups')
    
    users = list(objects) # consider records may be a generator
    membership = defaultdict(list)
    group_index = {}

    if action == 'create':
        for user in users: 
            print(f'{action.upper}: {user.username}')
            user.action = action
            for group in user.groups:
                group_index[group.name] = group
                membership[group.name].append(user)
            yield user

        # commands to add groups 
        for group_name, group in group_index.items():
            if group_name not in tio_groups:
                if action == 'create':
                    group.action = action
                    yield group

        # commands to modify group membership
        for group_name, members in membership.items():
            usernames = sorted([u.username for u in members])
            group = group_index[group_name]
            group.action = 'add_user'
            for member in members:
                yield group
    