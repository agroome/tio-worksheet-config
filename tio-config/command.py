from session import bind_method
from functools import wraps
import inspect

EXCLUDE_FROM_OUTPUT = {'password'}


class Command:
    def __init__(self, obj, method=None):
        print(f"command method: {method}")
        if method is None:
            method = obj.action
        self.method = method
        self._execute, self.params = bind_method(obj, method)
        self.obj = obj
        
    def execute(self, dry_run=False):
        param_str = ','.join([f'{k}="{v}"' for k, v in self.params.items() if k not in EXCLUDE_FROM_OUTPUT])
        class_name = self.obj.__class__.__name__
        # print(f'{self.method.upper()}: {class_name}({param_str})')
        print(f'{self.method.upper()}: {repr(self.obj)}')
        if not dry_run:
            return self._execute(**self.params)
        else:
            return {'method': self.method, 'params': self.params}


class BatchCommands:
    def __init__(self, objs, action):
        self.action = action
        print(f'building batch for: {action}')
        self.commands = [Command(obj, method=action) for obj in objs]

    def add_objs(self, objs):
        self.commands.extend([Command(obj, self.action) for obj in objs])

    def execute(self, dry_run=False):
        for command in self.commands:
            command.execute(dry_run=dry_run)

