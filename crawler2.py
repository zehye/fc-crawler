# 강사님 풀이
# 1. HTML 받아와서 html변수에 문자열을 할당
# 1-1. 만약 data/episode_list.html이 없다면
# -> 내장모듈 os의 'exists' 함수를 사용해본다. -> 파이썬 공식 문서 확인
# http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed
# 죽음에 관하여 (재) 페이지를 requests를 사용해서 data/episode_list.html에 저장
# list.nhn뒤 ? 부터는 url에 넣지 말고 get parameters로 처리
# -> requests문서의 'Passing Parameters In URLs'
# 저장 후에는 파일을 불러와 html 변수에 할당

# 1-2. 이미 data/episode_list.html이 있다면 html 변수에 파일을 불러와 할당

import os

from bs4 import BeautifulSoup
import requests

# HTML 파일을 저장하거나 불러올 경로
file_path = 'data/episode_list.html'
# HTTP 요청을 보낼 주소
url_episode_path = 'http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed'
# HTTP요청시 전달할 GET parameters
params = {'titleID': '703845', 'weekday': 'wed'}


# HTML 파일이 로컬에 저장되어 있는 지 검사
if os.path.exists(file_path):
    # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
    html = open(file_path, 'rt').read()

else:
    # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
    response = requests.get(url_episode_path, params)
    # 요청 응답객체의 text속성값을 html변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTMLVKDLFFH WJWKD
    open(file_path, 'wt').write(html)


# 2. 제목, 저자, 웹툰정보 탐색하기
#  html변수를 사용해 soup변수에 BeautifulSoup객체를 생성
#  soup객체에서
#    - 제목: 죽음에 관하여 (재)
#    - 작가: 시니/혀노
#    - 설명: 삶과 죽음의 경계선, 그 곳엔 누가 있을까의 내용을 가져와 title, author, description변수에 할당

soup = BeautifulSoup(html, 'lxml')

# div.detai > h2 (제목, 작가)의
# 0번째 자식: 제목 텍스트
# 1번째 자식: 작가정보 span tag
# tag로부터 문자열을 가져올때는 get_text()
h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
# strip=True : 문자열을 가져오는데 태그를 빈 공백으로 나누고 앞 뒤 공백 제거
#desc = soup.select_one('div.detail').h2.next_sibling
#div.detail > p (설명)
description = soup.select_one('div.detail > p').get_text(strip=True)
# url_thumbnail = soup.select_one('tr > a > img')
# td_title = soup.select_one('td.title > a')
#
# td_rating = soup.select_one('div.rating_type')
# rating1 = td_rating.content[1].get_text(strip=True)
# rating2 = td_rating.content[2].get_text(strip=True)
# create_date = soup.select_one('td.num').get_text(strip=True)
# print(desc)
# print(type(desc))
# print(desc.next_element)
print(title)
print(author)
print(description)
# print(url_thumbnail)
#print(h2_title)
# print(td_rating)
# print(rating1)
# print(rating2)
# print(create_date)


# 3. 에피소드 정보 목록을 가져오기
# url_thumnail: 썸네일 URL
# title: 제목
# rating: 별점
# create_date: 등록일
# no: 에피소드 상세페이지의 고유번호
# 각 에피소드들은 하나의 dict데이터
# 모든 에피소드들을 list에 넣는다

# 에피소드 목록을 담고 있는 table
table = soup.select_one('table.viewList')
#print(table.prettify())

# table내의 모든 tr요소 목록
tr_list = table.select('tr') # list로 반환 전체가 다 찾는 방법이 select

# 첫번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터
for index, tr in enumerate(tr_list[1:]):
    #print('==== {} =====\n{}\n'.format(index, tr))
    if tr.get('class'): # tr이 class를 가지면 제외하기 위해서 먼저 누가 가지고 있는지를 확인
        # 에피소드에 해당하는 tr은 클래스가 없으므로, 현재 순회중인 tr요소가
        # 클래스 속성값을 가진다면 continue
        continue
    #print(cls)

    # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
    url_thumnail = tr.select_one('td:nth-of-type(1) img').get('src')

    from urllib import parse
    # 현재 tr의 첫번째 td요소의 자식 a태그의 href'속성값
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    query_string = parse.urlsplit(url_detail).query
    # parse_qs : 스트링으로 주어진 쿼리를 해석한다, 공백같은 문자를 공백으로 두는게 아니라 %뒤의 취급할 수 있는 글로 변환
    query_dict = parse.parse_qs(query_string)
    no = query_dict['no'][0]

    # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    # 현재 tr의 네 번째 td요소의 내용
    create_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

    print(url_thumnail)
    #print(url_detail)
    print(title)
    print(rating)
    print(create_date)
    print(no)
