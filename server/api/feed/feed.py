from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Feeds

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, required=True, location='form')
post_parser.add_argument('lecture_id', type=int, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')

class Feed(Resource):
    
    @swagger.doc({
        'tags': ['feed'],
        'description': '게시글 등록하기',
        'parameters': [
            {
                'name' : 'user_id',
                'description' : '어느 사용자가 작성한 것인지',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True
            },
            {
                'name' : 'lecture_id',
                'description' : '어느 강의에 대해 작성한 것인지',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True
            },
            {
                'name' : 'content',
                'description' : '게시글 내용',
                'in' : 'formData',
                'type' : 'string',
                'required' : True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '게시글 등록 성공',
            },
            '400': {
                'description': '게시글 등록 실패',
            }
        }
    })
    
    def post(self) :        
        """게시글 등록하기"""
        
        args = post_parser.parse_args()
                
        return {
            '임시' : '게시글 등록'
        }