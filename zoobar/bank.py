from zoodb import *
from debug import *

import time
import auth_client

def transfer(sender, token, recipient, zoobars):
    if not auth_client.check_token(sender, token):
        return False

    bank_db = bank_setup()
    sender_account = bank_db.query(Account).get(sender)
    recipient_account = bank_db.query(Account).get(recipient)

    sender_balance = sender_account.zoobars - zoobars
    recipient_balance = recipient_account.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        return False

    sender_account.zoobars = sender_balance
    recipient_account.zoobars = recipient_balance
    bank_db.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()
    return True

def balance(username):
    db = bank_setup()
    account = db.query(Account).get(username)
    return account.zoobars

def get_log(username):
    db = transfer_setup()
    xfers = db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))
    return [dict(sender=x.sender, recipient=x.recipient, amount=x.amount, time=x.time) for x in xfers]

def new_account(username):
    account = Account()
    account.username = username
    db = bank_setup()
    db.add(account)
    db.commit()
