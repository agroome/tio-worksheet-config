import inspect
import logging
from functools import cache, partial, wraps
from tenable.io import TenableIO
from collections import defaultdict
import models

print("MODULE: session")
data_models = {}

class SessionNotInitialized(Exception):
    ''''''

class CacheNotImlpemented(Exception):
    ''''''

client: TenableIO = None

tio_api = defaultdict(lambda: defaultdict(dict))


def init(tio: TenableIO):
    global client
    client = tio
    init_api_catalog(client)
    return client


def init_api_catalog(client):
    api_classes = [(k, v) for k, v in inspect.getmembers(client) if not k.startswith('_')]
    for name, item in api_classes:
        if not inspect.ismethod(item):
            for _, method in inspect.getmembers(item):
                if inspect.ismethod(method):
                    params = inspect.signature(method).parameters
                    tio_api[name][method.__name__] = dict(method=method, params=params)


def get_sesion():
    if client is None:
        raise SessionNotInitialized('session needs to be initialized with init_session(tio)')
    return client


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
        raise AttributeError(f"[{obj.__class__.__name__}]: class must define 'api_name'")

    api_method, valid_parameters = get_api_method(api_name, method)
    if method == 'delete':
        params = {}
        func = partial(api_method, obj.id)
    else:
        params = {k: v for k, v in obj.dict().items() if k in valid_parameters}
        func = api_method

    return func, params


def bind_api(api_name):
    def outer(cls):
        if inspect.isclass(cls):
            print(f'registering {cls.__name__} api_name to {api_name}')
            cls.api_name = api_name
            data_models[api_name] = cls
        @wraps(cls)
        def inner(*args, **kwargs):
            obj = cls(*args, **kwargs)
            return obj
        return inner
    return outer


    

