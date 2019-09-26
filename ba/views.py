# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

from flask import render_template, session, request, url_for, redirect
from ba.models import User
from ba import app, sys, logic

@app.route('/index')
def index():
    rt = logic.getAllTeams()
    return render_template('index.html', teams = rt, user = sys.getLoginUser())

@app.route('/mytasks')
def mytask():
    userId = sys.getLoginUser().userId
    rt = logic.getTasksByUserId(userId)
    return render_template('task/mytask.html', tasks=rt, user = sys.getLoginUser())

@app.route('/myteams')
def myteam():
    userId = sys.getLoginUser().userId
    rt = logic.getTeamsByUserId(userId)
    return render_template('organization/myteam.html', tasks=rt, user = sys.getLoginUser())

@app.route('/login')
def login():
    return render_template('account/login.html')

@app.route('/loginAction', methods=['POST'])
def loginAction():

    username = request.form['username']
    password = request.form['password']
    rt = logic.loginByCredential(username, password)

    if len(rt) >= 1:
        sys.setLoginUser(rt[0]['UserId'], rt[0]['ClassName'], rt[0]['SchoolName'], rt[0]['WeChat'])
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
    
    