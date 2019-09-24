# -*- coding: utf-8 -*-
import os
from flask import Flask
from config import dbCfg
from flask_bootstrap import Bootstrap
from app.dbhelper import SqlHelper

app = Flask(__name__)
Bootstrap(app)
# app.config.from_object('config') # 载入配置文件
#db = SQLAlchemy(app) # 初始化 db 对象
db = SqlHelper(dbCfg['serverName'] , dbCfg['userName'] , dbCfg['passWord'], dbCfg['dbName'])

from app import views, models, db