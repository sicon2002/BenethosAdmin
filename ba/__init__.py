# -*- coding: utf-8 -*-
import os
from flask import Flask
from config import dbCfg, jobCfg
from flask_bootstrap import Bootstrap
# from app.helpers.dbhelper import *
from ba.helpers.utils import *
from ba.helpers.logic import *
from ba.helpers.jobs import *

from flask_apscheduler import APScheduler

scheduler = APScheduler()

app = Flask(__name__)
app.secret_key = "WhatIsYourSecretKey?"
Bootstrap(app)

# db = SqlHelper(dbCfg['serverName'] , dbCfg['userName'] , dbCfg['passWord'], dbCfg['dbName'])
sys = SysHelper()
logic = LogicHelper()

# # jobs go here
# app.config.update(jobCfg)
# scheduler.init_app(app)
# scheduler.start()

water_mark_handler()

from ba import app, views, models, sys, logic
