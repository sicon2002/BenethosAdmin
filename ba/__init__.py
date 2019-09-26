# -*- coding: utf-8 -*-
import os
from flask import Flask
from config import dbCfg
from flask_bootstrap import Bootstrap
# from app.helpers.dbhelper import *
from ba.helpers.utils import *
from ba.helpers.logic import *

app = Flask(__name__)
app.secret_key = "WhatIsYourSecretKey?"
Bootstrap(app)

# db = SqlHelper(dbCfg['serverName'] , dbCfg['userName'] , dbCfg['passWord'], dbCfg['dbName'])
sys = SysHelper()
logic = LogicHelper()

print("I'm here....")

from ba import app, views, models, sys, logic