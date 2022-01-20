from flask_restful import Resource

from server import db
from server.model import Users, LectureUser, Lectures

class AdminDashboard (Resource):
    
    def get(self):
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        
        
        # first() 한 줄, all() 목록, count() 검색된 갯수
        users_count = Users.query\
            .filter(Users.email != 'retired')\
            .count()
            
        # 연습 - 자바 강의의 매출 총액 => 집계함수 + (ORM) JOIN 활용
        
        # query( SELECT 컬럼 선택처럼 여러 항목 가능)
        # db.func.집계 함수(컬럼) => 집계 함수 동작
        
        # filter 나열 => JOIN / ON을 한 번에 명시
        # filter 나열 2 => JOIN이 끝나면 WHERE절처럼 실제 필터 조건
        
        # froup_by => 어떤 값을 기준으로 그룹 지을지 명시
        
        lecture_fee_amount = db.session.query( Lectures.title, db.func.sum(Lectures.fee) )\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .group_by(Lectures.id)\
            .all()
            
        # print(lecture_fee_amount)  => JSON 응답으로 내려갈 수 없다. 가공 처리 필요
        
        amount_list = [ {'lecture_title' : row[0], 'amount' : int(row[1]), }  for row in lecture_fee_amount ]
        
        
        # 남성 회원수 / 여성 회원수
        gender_user_count_list = db.session.query(Users.is_female, db.func.count(Users.id))\
            .group_by(Users.is_female)\
            .all()
            
        gender_user_count = [ {'is_female' : row[0], 'user_count' : int(row[1])}  for row in gender_user_count_list ]
                            
        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' :{
                'live_user_count' : users_count,
                'lecture_amount' : amount_list, # 각 강의별 총합
                'gender_user_counts' : gender_user_count,  # 성별에 따른 사용자 수
            }
        }