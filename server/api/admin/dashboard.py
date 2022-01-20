import datetime
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
            
        # 성별 사람 수 (탈퇴하지 않은)
        female = db.session.query(Users.is_female, db.func.count(Users.id))\
            .group_by(Users.is_female==True)\
            .filter( Users.retired_at == None)\
            .all()
            
        gender_user = []
        for row in female :
            gender_user.append ({
                'is_female' : row[0],
                'count' : row[1] 
            })
            
        # 일자별로 총 매출 금액
        amount_lecture_fee = db.session.query(Lectures.title, db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.created_at > '2022-01-10')\
            .group_by(db.func.date(LectureUser.created_at))\
            .all()
            
        print(amount_lecture_fee)
            
        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' :{
                'leave_users' : users_count,
                'amount_lecture' : amount_list,
                'count_peson' : gender_user,
            }            
        }