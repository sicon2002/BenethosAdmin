#--encoding:utf-8--
from flask import session
from ba.models import User
import random

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
        if 'USER_ONLINE' in session:
            userObj = session['USER_ONLINE']
            return User.toObject(userObj)
        else:
            return redirect(url_for('login'))
    
    def genGuid(self):
        # 6F9619FF-8B86-D011-B42D-00C04FC964FF
        g1 = random.sample('0123456789ZYXWVUTSRQPONMLKJIHGFEDCBA',8)
        g2 = random.sample('0123456789ZYXWVUTSRQPONMLKJIHGFEDCBA',4)
        g3 = random.sample('0123456789ZYXWVUTSRQPONMLKJIHGFEDCBA',4)
        g4 = random.sample('0123456789ZYXWVUTSRQPONMLKJIHGFEDCBA',4)
        g5 = random.sample('0123456789ZYXWVUTSRQPONMLKJIHGFEDCBA',12)
        return ''.join(g1) + ''.join(g2) + '-' + ''.join(g2) + '-' + ''.join(g3) + '-' + ''.join(g4) + '-' + ''.join(g5)

    def genRandomNumber(self, start, end):
        return random.randint(start, end)