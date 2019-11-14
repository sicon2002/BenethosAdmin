# --encoding:utf-8--
from ba.helpers.dbhelper import SqlHelper
from config import dbCfg
from ba.helpers.utils import SysHelper

class LogicHelper:
    version = 0.1

    def __init__(self):
        self.db = SqlHelper(
            dbCfg['serverName'], dbCfg['userName'], dbCfg['passWord'], dbCfg['dbName'])
        self.util = SysHelper()
        print('init sys logic...')

    # teams
    def getAllTeams(self):
        rt = self.db.queryAll('SELECT TOP 10 * FROM NE_Teams')
        return rt

    def getTeamsByUserId(self, uid):
        rt = self.db.queryAll(
            "SELECT \
                DISTINCT tm.Id, Name, tm.DeleterUserId AS IvtCode, tm.CreatorUserId, tm.LastModificationTime, p.ClassName AS CreatorName, p.SchoolName AS CreatorMobile, p.WeChat \
                FROM NE_Teams tm \
                INNER JOIN NE_TeamUsers tu ON tm.Id = tu.TeamID \
                INNER JOIN NE_Profiles p ON tm.CreatorUserId = p.Id \
                WHERE tu.ProfileID = %d" % (uid)
        )
        return rt

    def getTeamById(self, id):
        rt = self.db.queryAll(
            "SELECT * FROM NE_Teams \
                WHERE Id = %d" % (id)
        )
        return rt

    # account
    def loginByCredential(self, u, p):
        rt = self.db.queryAll(
            "SELECT TOP 1 * FROM NE_Profiles WHERE SchoolName='%s' AND Pwd='%s'" % (u, p))
        return rt

    def getUsersByTeamId(self, tid):
        rt = self.db.queryAll(
            "SELECT \
                DISTINCT p.Id, p.ClassName AS UserName, p.SchoolName AS Mobile, p.WeChat, tu.DeleterUserId AS IsMember \
                FROM NE_TeamUsers tu \
                INNER JOIN NE_Profiles p ON tu.ProfileID = p.Id \
                INNER JOIN AbpUsers u ON u.Id = p.ID \
                WHERE TeamID = %d" % (tid)
        )
        return rt

    # tasks
    def getTasksByUserId(self, uid):
        rt = self.db.queryAll(
            "SELECT \
                DISTINCT tsk.Id, Address, River, Name, EvaStatus, tsk.LastModificationTime \
                FROM NE_AppTasks tsk \
                INNER JOIN NE_Teams tm ON tsk.TeamID = tm.Id \
                INNER JOIN NE_TeamUsers tu ON tm.Id = tu.TeamID \
                WHERE tu.ProfileID = %d" % (uid)
        )
        return rt

    def getTaskById(self, id):
        rt = self.db.queryAll(
            "SELECT * FROM NE_AppTasks WHERE Id = %d" % (id)
        )
        return rt

    def getTaskDetailByTaskId(self, id):
        rt = self.db.queryAll(
            "SELECT \
              smp.BADict_Desc, BADict_ID, BADict_Value, BADict_ValType, BADict_ValueDesc, d.CategoryID, d.[Desc], d.Name \
            FROM NE_AppTasks tsk \
            INNER JOIN NE_AppTaskSamples smp ON tsk.Id = smp.TaskId \
            INNER JOIN NE_BADict d ON d.Id = smp.BADict_ID \
            WHERE tsk.Id = %d"%(id)
        )
        return rt

    def getAllImages(self):
        rt = self.db.queryAll(
            "SELECT s.id, BADict_ID, BADict_ValType,BADict_Value,s.DeleterUserId, s.TaskID, t.TeamId, tm.Name \
            FROM NE_AppTaskSamples s \
            INNER JOIN NE_BADict d ON s.BADict_ID = d.Id \
            INNER JOIN NE_AppTasks t ON t.Id = s.TaskId \
            INNER JOIN NE_Teams tm ON tm.Id = t.TeamID \
            WHERE d.CategoryID IN (7,8,13)  \
            AND (s.DeleterUserId IS NULL OR s.DeleterUserId <> 1) \
            "
        )
        return rt

    def updateImageHandleStatus(self, id, flg):
        rt = self.db.updateSql(
            "UPDATE NE_AppTaskSamples \
            SET DeleterUserId = %d \
            WHERE id = %d"%(flg, id)
        )
        return 'okay'

    # report
    def generateReport(self, taskid, userid):
        rptGuid = self.util.genGuid()
        rptNo = self.util.genRandomNumber(100000, 999999)

        sql = "INSERT INTO NE_Reports(TaskId, UserId, SeqNo, ReportType, ID, IsValid, CreateDate, Comments, GenTimes) \
            VALUES(%s,%s,%s,'%s','%s',1,'%s','',%s)"%(taskid, userid, rptNo, 'CMZX', rptGuid, '2019-11-11', 1)
            
        rt = self.db.updateSql(sql)
        return 'okay'

    def getReportByIds(self, taskid, userid):
        rt = self.db.queryAll(
            "SELECT * FROM NE_Reports \
            WHERE TaskId = %s AND UserId = %s"%(taskid, userid)
        )
        return rt

    def getReportByGuid(self, guid):
        rt = self.db.queryAll(
            "SELECT * FROM NE_Reports \
            WHERE ID = '%s'"%(guid)
        )
        return rt

    def increaseReportGenTimes(self, guid):
        rt = self.db.updateSql(
            "UPDATE NE_Reports \
            SET GenTimes = GenTimes+1 \
            WHERE ID = '%s'"%(guid)
        )
        return 'okay'

    def getTaskUserReportByTaskId(self, taskid):
        sql = "SELECT DISTINCT p.Id, p.ClassName AS UserName, p.SchoolName AS Mobile, p.Wechat, tu.DeleterUserId AS IsMember, r.ID AS RptGuid, r.ReportType, r.SeqNo, r.CreateDate, r.TaskId, r.Comments, r.IsValid, r.GenTimes \
            FROM NE_AppTasks t \
            INNER JOIN NE_TeamUsers tu ON tu.TeamId = t.TeamId \
            INNER JOIN NE_Profiles p ON p.Id = tu.ProfileId \
            LEFT JOIN NE_Reports r ON r.TaskId = t.Id AND r.UserId = p.Id \
            WHERE t.Id = %s"%(taskid)

        rt = self.db.queryAll(sql)
        return rt