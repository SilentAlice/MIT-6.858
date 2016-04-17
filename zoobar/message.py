from zoodb import *
from debug import *

import time
import auth_client

def send_message(sender, token, to, text):
    if not auth_client.check_token(sender, token):
        return False

    message = Message()
    message.sender = sender
    message.to = to
    message.text = text
    message.time = time.asctime()

    db = message_setup()
    db.add(message)
    db.commit()
    return True

def get_messages(username):
    db = message_setup()
    messages = db.query(Message).filter(Message.to==username)
    return [dict(sender=x.sender, to=x.to, text=x.text, time=x.time) for x in messages]
