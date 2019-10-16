#--encoding:utf-8--
#
import pymssql
 
class SqlHelper:
    version=0.1
    def __init__(self,servername,username,password,dbname):
        self.serverName=servername
        self.userName=username
        self.passWord=password
        self.dbName=dbname

        try:
            self.conn = pymssql.connect(self.serverName, self.userName, self.passWord, self.dbName)
            self.cursor = self.conn.cursor()
            print('init db success...')
        except pymssql.Error as e:
            print('Sql Error 001')
            print(e)

    def query(self,sql):
        try:
            rows=self.cursor.execute(sql)
            return rows;
        except pymssql.Error as e:
            print('Sql Error 002: %s SQL: %s'%(e,sql))
            
    # def queryOnlyRow(self,sql):
    #     try:
    #         self.query(sql)
    #         result=self.cursor.fetchone()
    #         desc=self.cursor.description
    #         row={}
    #         for i in range(0,len(result)):
    #             row[desc[i][0]]=result[i]
    #         return row;
    #     except MySQLdb.Error as e:
    #         print('MySql Error: %s SQL: %s'%(e,sql))
    
    def queryAll(self,sql):
        try:
            self.query(sql)
            result=self.cursor.fetchall()
            desc=self.cursor.description
            rows=[]
            for cloumn in result:
                row={}
                for i in range(0,len(cloumn)):
                    row[desc[i][0]]=cloumn[i]
                rows.append(row)  
            return rows
        except pymssql.Error as e:
            print('MySql Error 003: %s SQL: %s'%(e,sql))
        # finally:
        #     self.close()
    
    # def insert(self,tableName,pData):
    #     try:
    #         newData={}
    #         for key in pData:
    #             newData[key]="'"+pData[key]+"'"
    #         key=','.join(newData.keys())
    #         value=','.join(newData.values())
    #         sql="insert into "+tableName+"("+key+") values("+value+")"
    #         self.query("set names 'utf8'")
    #         self.query(sql)
    #         self.commit()
    #     except MySQLdb.Error as e:
    #         self.conn.rollback()
    #         print('MySql Error: %s %s'%(e.args[0],e.args[1]))
    #     finally:
    #         self.close()
    
    # def update(self,tableName,pData,whereData):
    #     try:
    #         newData=[]
    #         keys=pData.keys()
    #         for i in keys:
    #             item="%s=%s"%(i,"'"+pData[i]+"'")
    #             newData.append(item)
    #         items=','.join(newData)
    #         newData2=[]
    #         keys=whereData.keys()
    #         for i in keys:
    #             item="%s=%s"%(i,"'"+whereData[i]+"'")
    #             newData2.append(item)
    #         whereItems=" AND ".join(newData2)
    #         sql="update "+tableName+" set "+items+" where "+whereItems
    #         self.query("set names 'utf8'")
    #         self.query(sql)
    #         self.commit()
    #     except MySQLdb.Error as e:
    #         self.conn.rollback()
    #         print('MySql Error: %s %s'%(e.args[0],e.args[1]))
    #     finally:
    #         self.close()

    def updateSql(self,sql):
        try:
            #self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
        except pymssql.Error as e:
            #self.conn.rollback()
            print('MySql Error: %s %s'%(e,sql))
        # finally:
        #     self.close()
    
    # def getLastInsertRowId(self):
    #     return self.cursor.lastrowid
    
    # def getRowCount(self):
    #     return self.cursor.rowcount
    
    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.cursor.close()
        self.conn.close()