from flask_restful import Resource
from flask_restful_swagger_2 import swagger

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
        return {
            '임시' : '게시글 등록'
        }