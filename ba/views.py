# -*- coding: utf-8 -*-
import sys, datetime
sys.path.append("..")

from jinja2 import PackageLoader, Environment
import xhtml2pdf.pisa as pisa
from cStringIO import StringIO
from flask import render_template, session, request, url_for, redirect, current_app, make_response
from ba.models import User
from ba import app, sys, logic

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT



#filters
@app.template_filter('replace')
def fReplace(orgStr,targetStr,toStr):
    return orgStr.replace(targetStr,toStr)

@app.template_filter('format')
def fFormat(orgDate,t):
    if t == "s":
        return orgDate.strftime("%Y%m%d")
    else:
        return orgDate.strftime("%Y")+u"年"+orgDate.strftime("%m")+u"月"+orgDate.strftime("%d")

# indexs
@app.route('/index')
def index():
    return render_template('index.html', user = sys.getLoginUser())

# task
@app.route('/mytasks')
def mytask():
    userId = sys.getLoginUser().userId
    rt = logic.getTasksByUserId(userId)
    return render_template('task/mytask.html', tasks=rt, user = sys.getLoginUser())

@app.route('/task_report_mgr')
def task_report_mgr():
    return render_template('task/task_report_mgr.html', user = sys.getLoginUser())

@app.route('/task_detail/<tsk_id>')
def task_detail(tsk_id):
    tskId = int(tsk_id.encode("utf-8"))

    rtTaskInfo = logic.getTaskById(tskId)
    rtMembers = logic.getUsersByTeamId(rtTaskInfo[0]['TeamID'])
    rtMembersWithReportInfo = logic.getTaskUserReportByTaskId(tskId)
    return render_template('task/task_detail.html', taskInfo = rtTaskInfo[0], members = rtMembersWithReportInfo,  user = sys.getLoginUser())

# report
@app.route('/report/<guid>')
def report(guid):
    r = logic.getReportByGuid(guid)
    if(len(r) > 0):
        tskId = r[0]['TaskID']
        rtTaskInfo = logic.getTaskById(tskId)
        rtTeamInfo = logic.getTeamById(rtTaskInfo[0]['TeamID'])
        rtTeamMembers = logic.getUsersByTeamId(rtTaskInfo[0]['TeamID'])
        rtTaskSamples = logic.getTaskDetailByTaskId(tskId)

        return render_template('report/report.html', rptInfo = r[0], tskInfo = rtTaskInfo[0], teamInfo = rtTeamInfo[0], teamMembers = rtTeamMembers, tskSmps = rtTaskSamples )
    else:
        return "暂无报告，如有问题请与管理员联系！"

@app.route('/report/gen/<taskid>/<userid>')
def genReport(taskid, userid):
    rr = logic.getReportByIds(taskid, userid)
    print(rr)
    print(len(rr))
    if(len(rr) > 0):
        logic.increaseReportGenTimes(rr[0]["ID"])
    else:
        r = logic.generateReport(taskid, userid)
    return ''

# team
@app.route('/myteams')
def myteam():
    userId = sys.getLoginUser().userId
    rt = logic.getTeamsByUserId(userId)
    return render_template('organization/myteam.html', tasks=rt, user = sys.getLoginUser())

@app.route('/team_members')
def team_members():
    tid = 73
    rt = logic.getUsersByTeamId(tid)
    return render_template('organization/team_members.html', members=rt, user = sys.getLoginUser())

# sysconfig

@app.route('/jobmgr')
def taskmgr():
    return render_template('sysconfig/jobmgr.html', user = sys.getLoginUser())

# account
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

@app.route('/htmlpdf/<guid>', methods=['GET'])
def htmlpdf(guid):
    r = logic.getReportByGuid(guid)
    if(len(r) > 0):
        tskId = r[0]['TaskID']
        rtTaskInfo = logic.getTaskById(tskId)
        rtTeamInfo = logic.getTeamById(rtTaskInfo[0]['TeamID'])
        rtTeamMembers = logic.getUsersByTeamId(rtTaskInfo[0]['TeamID'])
        rtTaskSamples = logic.getTaskDetailByTaskId(tskId)

        return render_template('report/report_pdf.html', rptInfo = r[0], tskInfo = rtTaskInfo[0], teamInfo = rtTeamInfo[0], teamMembers = rtTeamMembers, tskSmps = rtTaskSamples )
    else:
        return "暂无报告，如有问题请与管理员联系！"

@app.route('/download/<guid>', methods=['GET'])
def download_pdf(guid):
    env = Environment(loader=PackageLoader(current_app.name, 'templates'))
    template = env.get_template('report/report_pdf.html') # 获得页面模板
    
    r = logic.getReportByGuid(guid)
    if(len(r) > 0):
        tskId = r[0]['TaskID']
        rtTaskInfo = logic.getTaskById(tskId)
        rtTeamInfo = logic.getTeamById(rtTaskInfo[0]['TeamID'])
        rtTeamMembers = logic.getUsersByTeamId(rtTaskInfo[0]['TeamID'])
        rtTaskSamples = logic.getTaskDetailByTaskId(tskId)

        fpath = current_app.root_path + '/fonts/simhei.ttf'
        
        html = template.render(rptInfo = r[0], tskInfo = rtTaskInfo[0], teamInfo = rtTeamInfo[0], teamMembers = rtTeamMembers, tskSmps = rtTaskSamples, font_path=fpath).encode('utf-8')
        
        pdfmetrics.registerFont(TTFont('yh', fpath))
        DEFAULT_FONT['helvetica'] = 'yh'

        result = StringIO()
        pdf = pisa.CreatePDF(StringIO(html), result)
        
        resp = make_response(result.getvalue())
        resp.headers["Content-Disposition"] = ("attachment; filename='{0}'; filename*=UTF-8''{0}".format('test.pdf'))
        resp.headers['Content-Type'] = 'application/pdf'
        return resp

        # return render_template('report/report.html', rptInfo = r[0], tskInfo = rtTaskInfo[0], teamInfo = rtTeamInfo[0], teamMembers = rtTeamMembers, tskSmps = rtTaskSamples )
    else:
        return "暂无报告，如有问题请与管理员联系！"
        

