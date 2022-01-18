import boto3
import time

from flask import current_app
from flask_restful import Resource,reqparse
from werkzeug.datastructures import FileStorage  # 파라미터로 파일을 받을 때 필요한 클래스
from flask_restful_swagger_2 import swagger

put_parser = reqparse.RequestParser()
# 파일을 받는 파라미터는 FileStorage, files에서 받아와야 함.  추가 행동 : append
put_parser.add_argument('profile_image', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('user_id', type=int, required=True, location='form')

class UserProfileImage(Resource):
    
    @swagger.doc({
        'tags': ['user'],  # 어떤 종류의 기능인지 분류.
        'description': '사용자 프로필 사진 등록',
        'parameters': [
            {
                'name' : 'user_id',
                'description' : '누구의  프사를 등록하는가?',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True
            },
            {
                'name' : 'profile_image',
                'description' : '실제로 첨부할 사진',
                'in' : 'formData',
                'type' : 'file',
                'required' : True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '프로필 사진 등록 성공',
            },
            '400': {
                'description': '프로필 사진 등록 실패',
            }
        }
    })
    def put(self) :
        """사용자 프로필 사진 등록"""
        
        args = put_parser.parse_args()
        
        # aws - s3에 어떤 키 / 비밀키를 들고 갈 지 세팅
        # 키 값들은 -> 환경 설정에 저장해둔 값을 불러와서 사용
        aws_s3 = boto3.resource('s3',\
            aws_access_key_id= current_app.config['AWS_ACCESS_KEY_ID'],\
            aws_secret_access_key= current_app.config['AWS_SECRET_ACCESS_KEY'])
        
        # 파일의 경우 보통 여러 장 첨부 가능
        # args['profile_image'] 는 => list로 구성된 경우가 많음
        
        for file in args['profile_image']:
            # file : 파일 이름 / 실제 이미지 등 본문이 분리된 형태
            
            # 파일 이름 저장됨 => S3 버킷에 저장될 경로 생성에 활용 -> 이름 중복 발생 소지 있음
            # 파일 이름은 재가공 (누가_언제), 확장자(.jpg)만 가져다 사용
            # ex. PC 카카오톡 파일 전송 -> 다운로드 : 보낸 파일 이름을 무시하고 KaKao_?????.jpg 등으로 받아짐
            
            # 1. 파일 이름 재가공
            
            user_email = 'test@test.com'  # 임시 이메일
            now = round(time.time() *10000)  # 현재 시간을 숫자값으로 표현. 중복을 피하기 위한 요소로  활용
            
            new_file_name = f"MYSNS_{user_email}_{now}"
            
            # 2. 확장자 추출
            
            # 최종 경로 => 1,2의 합체 + S3의 폴더 지정
            s3_file_path = f'images/profile_imgs/{file.filename}'   # 올라갈 경로 생성
            
            # 파일 본문도 따로 저장 => 실제로 S3 경로에 업로드
            file_body = file.stream.read()  # 올려줄 파일
            
            # 어떤 버킷에 올려줄 것인지 설정 => 파일 업로드
            aws_s3.Bucket(current_app.config['AWS_S3_BUCKET_NAME']).put_object(Key=s3_file_path, Body=file_body)
            
            # 사진 파일을 누구나 볼 수 있게 public 허용
            aws_s3.ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_path).put(ACL='public-read')
            
        return {
            '임시' : '사용자 프사 등록 기능'
        }