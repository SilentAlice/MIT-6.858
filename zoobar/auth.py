from zoodb import *
from debug import *

import hashlib
import random
import pbkdf2
import binascii
import bank_client

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == secure_hash(password, cred.salt):
        return newtoken(db, cred)
    else:
        return None

def secure_hash(password, salt):
    return pbkdf2.PBKDF2(password, salt).hexread(32)

def secure_salt():
    return binascii.hexlify(os.urandom(10))

def register(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred:
        return None
    newcred = Cred()
    newcred.username = username
    salt = secure_salt()
    newcred.salt = salt
    newcred.password = secure_hash(password, salt)
    db.add(newcred)
    db.commit()

    newperson = Person()
    newperson.username = username
    person_db = person_setup()
    person_db.add(newperson)
    person_db.commit()

    bank_client.new_account(username)

    return newtoken(db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

