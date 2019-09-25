# -*- coding: utf-8 -*-
import os
from flask import Flask
from config import dbCfg
from flask_bootstrap import Bootstrap
# from app.helpers.dbhelper import *
from app.helpers.utils import *
from app.helpers.logic import *

myapp = Flask(__name__)
myapp.secret_key = "WhatIsYourSecretKey?"
Bootstrap(myapp)

# db = SqlHelper(dbCfg['serverName'] , dbCfg['userName'] , dbCfg['passWord'], dbCfg['dbName'])
sys = SysHelper()
logic = LogicHelper()

from app import myapp, views, models, sys, logic