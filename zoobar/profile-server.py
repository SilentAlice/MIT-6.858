#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import hashlib
import socket
import bank_client
import zoodb
import binascii
import modify_profile_client
import message_client

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

def get_token(username):
    db = zoodb.cred_setup()
    cred = db.query(zoodb.Cred).get(username)
    return cred.token

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor, uid):
        self.user = user
        self.visitor = visitor
        self.token = get_token(user)
        os.setgroups([61012]) ## to open person db
        os.setresuid(uid, uid, uid)

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank_client.get_log(username):
            xfers.append({ 'sender': xfer.sender,
                           'recipient': xfer.recipient,
                           'amount': xfer.amount,
                           'time': xfer.time,
                         })
        return xfers

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        profile = modify_profile_client.get_profile(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': profile,
                 'zoobars': bank_client.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank_client.transfer(self.user, self.token, target, zoobars)

    def rpc_get_messages(self, username):
        # return [dict(sender="sender1", to=username, text="text1"), dict(sender="sender2", to=username, text="text2")]
        return message_client.get_messages(username)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, user, visitor):
        uid = 61017
        api_uid = 61018

        userdir = '/tmp/profilesvc/' + binascii.hexlify(user)
        mkdirs(userdir)
        os.chown(userdir, uid, uid)

        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor, api_uid).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')

        pcode = modify_profile_client.get_profile(user)
        pcode = pcode.encode('ascii', 'ignore')
        pcode = pcode.replace('\r\n', '\n')

        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
