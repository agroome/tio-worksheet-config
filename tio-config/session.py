
from tenable.io import TenableIO
from functools import cache, partial, wraps
import inspect
import logging

class SessionNotInitialized(Exception):
    ''''''

class CacheNotImlpemented(Exception):
    ''''''

session: TenableIO = None

def init(s: TenableIO):
    global session
    print("init session ")
    session = s


def get_sesion():
    if session is None:
        raise SessionNotInitialized('session needs to be initialized with init_session(tio)')
    return session


@cache
def get_api_method(api, method):
    tio_client = get_sesion()
    api_cls = getattr(tio_client, api)
    if api_cls is None:
        raise AttributeError(f"[TenableIO{api}] api not found")

    api_method = getattr(api_cls, method)
    if api_method is None:
        raise NotImplementedError(f"[TenableIO.{api}.{method}]")
    return api_method, list(inspect.signature(api_method).parameters)
            

# def bind_execute_method(obj, method):
#     try:
#         api_name = obj.api_name
#     except AttributeError as e:
#         raise AttributeError(f"[{obj.__name__}]: class must define 'api_name'")

#     api_method, valid_parameters = get_api_method(api_name, method)
#     if method == 'delete':
#         func = partial(api_method, obj.id)
#     else:
#         params = {k: v for k, v in obj.dict().items() if k in valid_parameters}
#         print(f'binding {api_method} to {params}')
#         func = partial(api_method, **params)

#     return func


# def api_binding(f):
#     @wraps(f)
#     def inner(func, data_model, *args, **kwargs):
#         api_method, valid_parameters = get_api_method(data_model.api_type, data_model.action)
#         parameters = {k: v for k, v in data_model if k in valid_parameters}
#         logging.DEBUG('calling %s params %s', api_method, ','.join(list(parameters)))
#         return f(api_method, parameters, *args, **kwargs)
        
#     return inner



@cache
def get_cached(resource: str) -> dict:
    session = get_sesion()
    if resource == 'users':
        users = {user['user_name'].lower(): user for user in session.users.list()}
        return users
    elif resource == 'groups':
        return {group.get('name'): group for group in session.groups.list()}
    elif resource == 'asset_tag_filters':
        return session.filters.asset_tag_filters()
    raise IndexError(f'[{resource}]: no cache')

def bind_method(obj, method):
    try:
        api_name = obj.api_name
    except AttributeError as e:
        raise AttributeError(f"[{obj.__name__}]: class must define 'api_name'")

    api_method, valid_parameters = get_api_method(api_name, method)
    if method == 'delete':
        print(api_method, obj.id)
        params = {}
        print(f'delete id={obj.id}')
        func = partial(api_method, obj.id)
    else:
        params = {k: v for k, v in obj.dict().items() if k in valid_parameters}
        print(f'binding {api_method} to {params}')
        func = api_method

    return func, params


class Command:
    def __init__(self, obj, method=None):
        if method is None:
            method = obj.action
        self.method = method
        self._execute, self.params = bind_method(obj, method)
        self.obj = obj
        
    def execute(self):
        print(f'execute {self.method} with {self.params}')
        return self._execute(**self.params)
            




