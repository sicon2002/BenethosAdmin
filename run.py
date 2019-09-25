# -*- coding: utf-8 -*-
from app import myapp

if __name__ == '__main__':
    myapp.debug = True # 设置调试模式，生产模式的时候要关掉debug
    myapp.run() # 启动服务器

    