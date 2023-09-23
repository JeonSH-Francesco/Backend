from flask import Flask

app=Flask(__name__)
#import 한 Flask 클래스를 객체화 시켜서 app이라는 변수에 저장 API의 설정과 엔드포인트들을 추가

#decorator를 사용하여 엔드포인트를 등록한다.
# 이 경우에는 그 다음에 나오는 ping 함수를 엔드포인트 함수로 등록
@app.route('/ping',methods=['GET'])
#ping 함수 정의 단순 문자열 pong 반환
#Flask가 알아서 HTTP response로 변환해서 HTTP request를 보낸 클라이언트에게 전송한다.
def ping():
    return "pong"
if __name__ == '__main__':
    app.run()
