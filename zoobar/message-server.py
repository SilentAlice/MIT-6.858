#!/usr/bin/python

import rpclib
import sys
import message
from debug import *

class MessageRpcServer(rpclib.RpcServer):
    def rpc_send_message(self, sender, token, to, text):
        return message.send_message(sender, token, to, text)

    def rpc_get_messages(self, username):
        return message.get_messages(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = MessageRpcServer()
s.run_sockpath_fork(sockpath)
