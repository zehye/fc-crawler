# 우리가 웹 브라우저를 통해 보는 HTML문서는 GET요청의 결과
# requests를 사용해 http://comic.naver.com/webtoon/weekday.nhn 주소에 get요청
# 요청결과를 response변수에 할당해서 status_code속성을 출력

import requests

response = requests.get('http://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)

# http get요청으로 받아온 content를 text데이터로 리턴
print(response.text)

# response.text에 해당하는 데이터를 weekday.html이라는 파일에 기록
# 다 기록했으면 close()호출
with open('weekday.html', 'wt') as f:
    f.write(response.text)
