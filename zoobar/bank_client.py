from debug import *
from zoodb import *
import rpclib

def transfer(sender, token, recipient, zoobars):
    with rpclib.client_connect('/banksvc/sock') as c:
        if not c.call('transfer', sender=sender, token=token, recipient=recipient, zoobars=zoobars):
            raise ValueError()

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('balance', username=username)

def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        xfers = c.call('get_log', username=username)
        return [TransferJSON(x['sender'], x['recipient'], x['amount'], x['time']) for x in xfers]

def new_account(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('new_account', username=username)
