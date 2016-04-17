#!/usr/bin/python

import rpclib
import sys
import modify_profile
from debug import *

class ModifyProfileRpcServer(rpclib.RpcServer):
    def rpc_modify_profile(self, username, token, profile):
        return modify_profile.modify_profile(username, token, profile)

    def rpc_get_profile(self, username):
        return modify_profile.get_profile(username)

    def rpc_add_user(self, username):
        return modify_profile.add_user(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ModifyProfileRpcServer()
s.run_sockpath_fork(sockpath)
