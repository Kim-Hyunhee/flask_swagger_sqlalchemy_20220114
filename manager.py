#  서버를 구동시키는 역할
#  디버그 / 테스트 / 라이브 모드 설정 => flask_script 라이브러리 활용

from flask_script import Manager

from server import creat_app


# 특별한 설정이없다면 => 실제 환경이 기본 설정
app = creat_app('ProductionConfig')

# 실제 설정으로 만들어둔 앱 => 매니저의 도움을 받아서 열도록 세팅
manager = Manager(app)

# 파이썬 명령어로 실행할 때 추가 키워드를 받아서 실행
# python manager.py "추가 키워드"

@manager.command
def debug():
    #"추가 키워드 "=> debug
    # 디버그 환경으로 잡아서 서버 실행
    app.config.from_object('server.config.DebugConfig')
    app.run(host='0.0.0.0')

@manager.command
def runserver():
    #"추가 키워드 "=> runserver
    # 기본 세팅 그대로 서버 실행
    app.run(host='0.0.0.0')
    
# 이 파일이 실행될 때 -> 매니저의 커맨드를 기반으로 실행되게 세팅을 해야함
# 파이썬 명령어로 이 파일을 실행 시켰는지?
if __name__ == '__main__':
    manager.run()