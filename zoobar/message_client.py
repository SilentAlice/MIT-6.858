from debug import *
from zoodb import *
import rpclib

def send_message(sender, token, to, text):
    with rpclib.client_connect('/messagesvc/sock') as c:
        if not c.call('send_message', sender=sender, token=token, to=to, text=text):
            raise ValueError()

def get_messages(username):
    with rpclib.client_connect('/messagesvc/sock') as c:
        return c.call('get_messages', username=username)
