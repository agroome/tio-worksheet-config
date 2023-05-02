import session
import inspect

from collections import defaultdict

tio_api = defaultdict(lambda: defaultdict(dict))

def init_api_catalog(client):
    api_classes = [(k, v) for k, v in inspect.getmembers(client) if not k.startswith('_')]
    for name, item in api_classes:
        if not inspect.ismethod(item):
            for _, method in inspect.getmembers(item):
                if inspect.ismethod(method):
                    params = inspect.signature(method).parameters
                    tio_api[name][method.__name__] = dict(method=method, params=params)


init_api_catalog(session.client)
    

