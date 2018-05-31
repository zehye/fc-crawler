import os
from urllib import parse

import requests
from bs4 import BeautifulSoup
class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        url = 'https://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url
        # print(parse.urlencode(params))
        # print(episode_url)

def webtoon_crawler(webtoon_id):
    """
   webtoon_id 를 입력받아서 웹툰 title, author,description 을 넘겨주는 함수
   :param webtoon_id:
   :return:
   """
    # HTML파일을 저장하거나 불러올 경로
    file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)
    # HTTP요청을 보낼 주소
    url_episode_list = 'http://comic.naver.com/webtoon/detail.nhn'
    # HTTP요청시 전달할 GET Parameters
    params = {
        'titleId': webtoon_id,
    }
    # -> 'http://com....nhn?titleId=703845

    # HTML파일이 로컬에 저장되어 있는지 검사
    if os.path.exists(file_path):
        # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
        html = open(file_path, 'rt').read()
    else:
        # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
        response = requests.get(url_episode_list, params)
        print(response.url)
        # 요청 응답객체의 text속성값을 html변수에 할당
        html = response.text
        # 받은 텍스트 데이터를 HTML파일로 저장
        open(file_path, 'wt').write(html)

    # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
    soup = BeautifulSoup(html, 'lxml')

    # div.detail > h2 (제목, 작가)의
    #  0번째 자식: 제목 텍스트
    #  1번째 자식: 작가정보 span Tag
    #   Tag로부터 문자열을 가져올때는 get_text()
    h2_title = soup.select_one('div.detail > h2')
    title = h2_title.contents[0].strip()
    author = h2_title.contents[1].get_text(strip=True)
    # div.detail > p (설명)
    description = soup.select_one('div.detail > p').get_text(strip=True)

    # print(title)
    # print(author)
    # print(description)

    # 웹툰 크롤링을 통해 얻게된 정보를 딕셔너리 형태로 return
    info = dict()
    info['title'] = title
    info['author'] = author
    info['description'] = description

    return info

def episode_crawler(webtoon_id):
    """
    웹툰 아이디를 입력받아서 웹툰 아이디, 타이틀, 넘버, 평점, 업데이트날짜 등
    이런 정보들을 가져오는 크롤러
    :param webtoon_id:
    :return:
    """
    # 에피소드 목록을 담고 있는 table
    # HTML파일을 저장하거나 불러올 경로
    file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)

    # HTML파일이 로컬에 저장되어 있는지 검사
    if os.path.exists(file_path):
        # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
        html = open(file_path, 'rt').read()

    # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select_one('table.viewList')
    # table내의 모든 tr요소 목록
    tr_list = table.select('tr')

    # list를 리턶기 위해 선언
    # for 문을 다 실행하면 episode_lists에는 Episode인스턴스가 들어가 있음
    episode_lists = list()

    # 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
    for index, tr in enumerate(tr_list[1:]):
        # 에피소드에 해당하는 tr은 클래스가 없으므로,
        # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
        if tr.get('class'):
            continue

        # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
        url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
        # 현재 tr의 첫 번째 td요소의 자식   a태그의 'href'속성값
        from urllib import parse
        url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
        query_string = parse.urlsplit(url_detail).query
        query_dict = parse.parse_qs(query_string)
        # print(query_dict)
        no = query_dict['no'][0]

        # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
        title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
        # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
        rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
        # 현재 tr의 네 번째 td요소의 내용
        created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

        # print(url_thumbnail)
        # print(title)
        # print(rating)
        # print(created_date)
        # print(no)

        new_episode = Episode(
            # 크롤링한 결과를 에피소드 클래스의 뉴 에피소드 인스턴스로 생성
            # 에피소드 클래스에 인스턴스들을 만든것
            webtoon_id=webtoon_id,
            no=no,
            url_thumbnail =url_thumbnail,
            title=title,
            rating = rating,
            created_date = created_date,
        )

        # episode_lists에 Episode인스턴스를 추가
        episode_lists.append(new_episode)
        #print(episode_lists)
        # 이 정보들을 넣고 새로운 인스턴스들을 만든다.

    return episode_lists

# ep = episode_crawler(703845)
# print(q)
# for item in ep:
#     print(item.no, item.title)

class Webtoon:
    def __init__(self, webtoon_id):
        # 웹툰 아이디만 가져와서 크롤러를 통해 나머지를 가져올 수 있도록 하기 위해 webtoon_id만 가져옴
        self.webtoon_id = webtoon_id
        # webtoon속성 채우기 위해 webtoon_crawler 함수 실행
        # webtoon_crawler함수 결과 dict()형태의 정보들
        info = webtoon_crawler(webtoon_id)
        #print(info)
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']
        self.episode_list = list()

    def update(self):
        """
        update함수를 실행하면 해당 웹툰 아이디에 따른 에피소드 정보들을
        에피소드 인스턴스로 저장
        :return:
        """

        result = episode_crawler(self.webtoon_id)
        # print(result)
        self.episode_list = result



# webtoon1 = Webtoon(703845)
# print(webtoon1.title)
# # print(webtoon1.episode_list)
# webtoon1.update()
# print(webtoon1.episode_list)

if __name__ == '__main__':

    webtoon2 = Webtoon(651673)
    print(webtoon2.title)
    webtoon2.update()
# print(webtoon2.title)

    for episode in webtoon2.episode_list:
        print(episode.url)