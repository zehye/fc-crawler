# 1. HTML 받아와서 html변수에 문자열을 할당
# 1-1. 만약 data/episode_list.html이 없다면
# -> 내장모듈 os의 'exists' 함수를 사용해본다. -> 파이썬 공식 문서 확인
# http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed
# 죽음에 관하여 (재) 페이지를 requests를 사용해서 data/episode_list.html에 저장
# list.nhn뒤 ? 부터는 url에 넣지 말고 get parameters로 처리
# -> requests문서의 'Passing Parameters In URLs'
# 저장 후에는 파일을 불러와 html 변수에 할당

# 1-2. 이미 data/episode_list.html이 있다면 html 변수에 파일을 불러와 할당

# 2. 제목, 저자, 웹툰정보 탐색하기
# html변수를 사용해 soup변수에 Beautifulsoup

import requests
# os.path.exists를 하기 위해서는 import os를 해줘야한다.
from bs4 import BeautifulSoup
import os

# os.path경로에 ()에 들어가는 파일이 exists(존재)하는지 안하는지를 알기 위해서는 if-else문을 사용해 확인할 수 있다.
# example을 통해서 해당 문법을 어떻게 사용하는 지 알아볼 수 있으니, example을 통해서 찾는 방법을 항상 생각하자.
if os.path.exists('data/episode_list.html'):
    # html이라는 벼수에 'data/episode_list.html파일을 읽기 형식으로 불러온다.
    html = open('data/episode_list.html').read()

else:
    # passing parameters를 하는 방법으로 본래 주소가
    # http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed 라면
    # payload = {'titleID': '703845', 'weekday':'wed'}
    # 즉 payload라는 변수에 위와 같이 딕셔너리를 구성한다. {'key1':'value1', 'key2':'value2'}
    payload = {'titleID': '703845', 'weekday': 'wed'}
    # response라는 변수에 requests를 통해 해당 주소에 get요청
    response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
    # html이라는 변수에 requests.get요청 받은 것을 text형식으로 변환하여 받는다.
    html = response.text

    # response.text에 해당하는 html 데이터를 data/episode_list.html이라는 파일에 기록한다.
    with open('data/episode_list.html', 'wt') as f:
        f.write(response.text)


soup = BeautifulSoup(html, 'lxml')


#title = soup.find('h2', class_="detail")
print(soup.find('div', class_="detail"))
# author = title.find('span', class_="wrt_nm")
# description = author.find_all('p')