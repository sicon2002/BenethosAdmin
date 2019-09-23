# -*- coding: utf-8 -*-
from flask import render_template, session
from app import app, db

@app.route('/')
def index():
    rlt = db.queryAll('SELECT TOP 10 * FROM NE_Teams')
    try:
        for item in rlt:
            print item['Name']
    except:
        print ''
    return render_template('index.html', teams = rlt)

@app.route('/login')
def login():
    return render_template('account/login.html')