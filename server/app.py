from flask import Flask
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
# DB 담당 라이브러리 import
from flask_sqlalchemy import SQLAlchemy

# DB 연결 전담 변수를 만들고 => import로 찾아다 쓸 수 있게 세팅
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    # 만들어진 앱에 (server>config>환경 설정 클래스) 환경 설정 불러오기
    app.config.from_object(f'server.config.{config_name}')
    
    # SQL Alchemy 세팅 진행 => 플라스크에 해둔 세팅값 (환경 설정 값) 을 불러다가 활용
    db.init_app(app)
    
    # 클래스 > 함수들을 자동으로 기능으로 연결해주는 라이브러리 세팅, 부가 환경 설정도 진행
    api = Api(app, api_spec_url='/api/spec', title='my_server_spec', api_version='0.1', catch_all_404s=True)
    
    from server.api.user import User
    from server.api.lecture import Lecture, LectureDetail
    from server.api.feed import Feed
    
    # api 폴더에서 만든 User 클래스를 가져다가 => /user로 접속 가능하게 등록
    api.add_resource(User, '/user')
    api.add_resource(Lecture, '/lecture')
    api.add_resource(LectureDetail, '/lecture/<int:lecture_id>')  # /lecture/숫자를 => int로 분석해서 lecture_id 변수에 담자
    api.add_resource(Feed, '/feed' )
    
    # swagger 문서를 자동 생성
    
    swagger_ui = get_swaggerui_blueprint('/api/docs','/api/spec.json', config={'app_name': 'my_sns_service'})
    
    # 플라스크 앱에 url에 swagger 문서를 등록
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')
    
    return app