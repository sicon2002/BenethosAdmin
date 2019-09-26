#--encoding:utf-8--
from ba.helpers.dbhelper import SqlHelper
from config import dbCfg

class LogicHelper:
    version=0.1
    def __init__(self):
        self.db = SqlHelper(dbCfg['serverName'] , dbCfg['userName'] , dbCfg['passWord'], dbCfg['dbName'])
        print('init sys logic...')

    def getAllTeams(self):
        rt = self.db.queryAll('SELECT TOP 10 * FROM NE_Teams')
        return rt
    
    def loginByCredential(self, u, p):
        rt = self.db.queryAll("SELECT TOP 1 * FROM NE_Profiles WHERE SchoolName='%s' AND Pwd='%s'"%(u,p))
        return rt
        
    def getTasksByUserId(self, uid):
        rt = self.db.queryAll(
                "SELECT \
                    DISTINCT tsk.Id, Address, River, Name, EvaStatus, tsk.LastModificationTime \
                FROM NE_AppTasks tsk \
                INNER JOIN NE_Teams tm ON tsk.TeamID = tm.Id \
                INNER JOIN NE_TeamUsers tu ON tm.Id = tu.TeamID \
                WHERE tu.ProfileID = %d"%(uid)
            )
        return rt

    def getTeamsByUserId(self, uid):
        rt = self.db.queryAll(
            "SELECT \
                DISTINCT tm.Id, Name, tm.DeleterUserId AS IvtCode, tm.CreatorUserId, tm.LastModificationTime, p.ClassName AS CreatorName, p.SchoolName AS CreatorMobile, p.WeChat \
            FROM NE_Teams tm \
            INNER JOIN NE_TeamUsers tu ON tm.Id = tu.TeamID \
            INNER JOIN NE_Profiles p ON tm.CreatorUserId = p.Id \
            WHERE tu.ProfileID = %d"%(uid)
        )
        return rt
            