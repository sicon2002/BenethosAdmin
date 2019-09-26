#--encoding:utf-8--
from flask import session
from ba.models import User

class SysHelper:
    version=0.1
    def __init__(self):
        print('init sys helpers...')

    def getSystime(self):
        return "213 sys helpers..."

    def setLoginUser(self, uid, username, mobile, nickname):
        user = User(uid, username, mobile, nickname)
        session['USER_ONLINE'] = user.toString()
        return True
    
    def getLoginUser(self):
        userObj = session['USER_ONLINE']
        return User.toObject(userObj)