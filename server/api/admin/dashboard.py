from flask_restful import Resource
from server import db
from server.model import Users

class AdminDashboard (Resource):
    
    def get (self):
        users_count = Users.query\
            .filter(Users.retired_at == None)\
            .count()
    
    
        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' :{
                'leave_users' : users_count
            }
            
        }