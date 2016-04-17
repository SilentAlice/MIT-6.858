from debug import *
from zoodb import *
import rpclib

def modify_profile(username, token, profile):
    with rpclib.client_connect('/modifyprofilesvc/sock') as c:
        if not c.call('modify_profile', username=username, token=token, profile=profile):
            raise ValueError()

def get_profile(username):
    with rpclib.client_connect('/modifyprofilesvc/sock') as c:
        return c.call('get_profile', username=username)

def add_user(username):
    with rpclib.client_connect('/modifyprofilesvc/sock') as c:
        return c.call('add_user', username=username)
