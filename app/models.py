
class User:
    version=0.1
    def __init__(self,userId,userName,mobile,nickName):
        self.userId=userId
        self.userName=userName
        self.mobile=mobile
        self.nickName=nickName
    
    def toString(self):
        return {
            'UserID':self.userId, 
            'UserName':self.userName, 
            'Mobile':self.mobile, 
            'NickName':self.nickName
        }

    @classmethod
    def toObject(self, objString):
        
        self.userId=objString['UserID']
        self.userName=objString['UserName']
        self.mobile=objString['Mobile']
        self.nickName=objString['NickName']

        return self