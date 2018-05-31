import requests
import os
from bs4 import BeautifulSoup


def webtoon_crawler(webtoon_id):
    # 사용자가 무조건 웹툰 아이디를 보내줘야 하는데,
    """
    webtoon_id를 입력받아서 웹툰 title, author, description을 넘겨주는 함수
    :param webtoon_id:
    :return:
    """
    file_path = 'data/new_episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)
    url_episode_path = 'http://comic.naver.com/webtoon/list.nhn'
    params = {'titleID': webtoon_id, }

    if os.path.exists(file_path):
        html = open(file_path, 'rt').read()

    else:
        response = requests.get(url_episode_path, params)
        html = response.text
        open(file_path, 'wt').write(html)

    soup = BeautifulSoup(html, 'lxml')

    title = soup.select_one('div.detail > h2')

    real_title = title.contents[0].strip()
    author = title.contents[1].get_text(strip=True)
    description = soup.select_one('div.detail > p').get_text(strip=True)

    print(real_title)
    print(author)
    print(description)

q = webtoon_crawler(651673)
print(q)

class Webtoon:
    def __init__(self, webtoon_id):
        # 웹툰 아이디만 가져와서 크롤러를 통해 나머지를 가져올 수 있도록 하기 위해 webtoon_id만 가져옴
        self.webtoon_id = webtoon_id
        self.title
        self.author
        self.description
        self.episode_list = list()

    def update(self):
        pass


class Episode:
    def __init__(self, webtoon_id, no, url_thunmnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumnail = url_thunmnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        pass
