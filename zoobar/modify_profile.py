from zoodb import *
from debug import *

import time
import auth_client

def modify_profile(username, token, profile):
    if not auth_client.check_token(username, token):
        return False

    db = profile_setup()
    record = db.query(Profile).get(username)
    record.profile = profile
    db.commit()
    return True

def get_profile(username):
    db = profile_setup()
    record = db.query(Profile).get(username)
    return record.profile

def add_user(username):
    record = Profile()
    record.username = username
    db = profile_setup()
    db.add(record)
    db.commit()
    return True
