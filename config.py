# -*- coding: utf-8 -*-
import os

#basedir = os.path.abspath(os.path.dirname(__file__))
dbCfg = {
    # database
    'serverName': '127.0.0.1',
    'userName': 'sa',
    'passWord': '1234qwer!@#$QWER',
    'dbName': "BA"
}

jobCfg = {"SCHEDULER_API_ENABLED": True,
          "JOBS": [{"id": "JOB_WATER_MARK",  # 任务ID
                    "func": "ba.helpers.jobs:water_mark_handler",  # 任务位置
                    "trigger": "interval",  # 触发器
                    "seconds": 10  # 时间间隔
                    }
                   ]
          }
