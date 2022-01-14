#  서버를 구동시키는 역할
#  디버그 / 테스트 / 라이브 모드 설정 => flask_script 라이브러리 활용

from server import creat_app

# 특별한 설정이없다면 => 실제 환경이 기본 설정
app = creat_app('ProductionConfig')

# 디버그 모드 => 파이썬 파일을 저장하면 => 서버도 자동 재시작

app.run(host='0.0.0.0')