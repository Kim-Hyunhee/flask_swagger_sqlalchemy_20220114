from flask_restful import Resource
from server import db
from server.model import Users, Lectures, LectureUser

class AdminDashboard (Resource):
    
    def get (self):
        users_count = Users.query\
            .filter(Users.retired_at == None)\
            .count()
    
    # 연습 - 자바 강의의 총 매출
    
    
        amount_lecture = db.session.query(Lectures.title, db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .group_by(Lectures.id)\
            .all()
            
        amount_list = []
        for row in amount_lecture:
            amount_list.append ({
                'lecture_title' : row[0],
                'amount' : int(row[1])
            })
        
            
        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' :{
                'leave_users' : users_count,
                'amount_lecture' : amount_list
            }
            
        }