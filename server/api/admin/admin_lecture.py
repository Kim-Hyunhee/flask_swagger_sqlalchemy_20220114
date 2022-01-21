from flask_restful import Resource,reqparse
from server import db
from server.model import Lectures

from flask_restful_swagger_2 import swagger

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('campus', type=str, required=True, location='form')
post_parser.add_argument('fee', type=int, required=True, location='form')

class AdminLecture (Resource):
    
    @swagger.doc({
        'tags' : ['admin'],
        'description' : '강의 추가하기',
        'parameter' : [
            {
                'name': 'X-Http-Token',
                'description': '어느 사용자인지를, 토큰으로',
                'in': 'header',
                'type': 'string',
                'required': True
            },
            {
                'name': 'title',
                'description': '강의 제목',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            {
                'name': 'campus',
                'description': '강의 하는 곳',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            {
                'name': 'fee',
                'description': '강의료',
                'in': 'formData',
                'type': 'integer',
                'required': True
            },
        ]
    })
    def post (self):
        """관리자 - 강의 추가 등록"""
        
        args = post_parser.parse_args()
        
        lecture = Lectures()
        lecture.title = args['title']
        lecture.campus = args['campus']
        lecture.fee = args['fee']
        
        db.session.add(lecture)
        db.session.commit()
        
        return {
            'code' : 200,
            'message' : '강의 등록 성공',
            
        }