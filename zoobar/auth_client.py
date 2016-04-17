from debug import *
from zoodb import *
import rpclib

def login(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        return c.call('login', username=username, password=password)

def register(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        return c.call('register', username=username, password=password)

def check_token(username, token):
    with rpclib.client_connect('/authsvc/sock') as c:
        return c.call('check_token', username=username, token=token)

