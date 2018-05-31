import os
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
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

        episode_url = url + urlencode(params)
        # urllib 보고 urlencode봤는데도 잘 이해가 안간다ㅠㅠㅠㅠㅠㅠㅠ
        return episode_url


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        info = self.webtoon_crawler()
        # class는 자기 내부에서 독립적인 스코프를 가지는데, <이 부분 강의 다시듣기>
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']
        self.episode_list = list()

    def webtoon_crawler(self):
        # staticmethod는 다른 인스턴스 메서드를 참조하지 않는다.
        """
        자기 자신이 가지고 있는 self.webtoon_id 를 그래도 쓸 수 있어, 클래스의 인스턴스 메서드로 존재하니까
        웹툰 title, author,description을 딕셔너리로 넘겨주는 함수
        """

        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        # file_path 바뀐부분 참고!
        url_episode_list = 'http://comic.naver.com/webtoon/detail.nhn'
        params = {
            'titleId': self.webtoon_id,
        }

        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:

            response = requests.get(url_episode_list, params)
            print(response.url)
            html = response.text
            open(file_path, 'wt').write(html)

        soup = BeautifulSoup(html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        # print(title)
        # print(author)
        # print(description)

        info = dict()
        # 웹툰의 정보를 딕셔너리 형태로 받아준다.(title, author, description)
        info['title'] = title
        info['author'] = author
        info['description'] = description

        return info
        # return된 info안에는 웹툰의 title, author, description정보가 들어가있다.
        # 이렇게 return된 info값은 class Webtoon에 활용된다.

    def episode_crawler(self):
        """
        webtoon_id를 매개변수로 입력받아서
        webtoon_id, title, url_thumbnail, no, rating, created_date의 정보를 가져오는 크롤러 함수
        :return:
        """
        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        # file_path 바뀐 부분 참고
        url_episode_list = 'http://comic.naver.com/webtoon/detail.nhn'
        params = {
            'titleId': self.webtoon_id,
        }

        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:

            response = requests.get(url_episode_list, params)
            print(response.url)
            html = response.text
            open(file_path, 'wt').write(html)

        soup = BeautifulSoup(html, 'lxml')
        table = soup.select_one('table.viewList')
        tr_list = table.select('tr')

        episode_lists = list()
        # for문 바깥에서 episode_lists라는 빈 리스트를 만든다.

        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue

            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')

            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            no = query_dict['no'][0]

            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            # print(url_thumbnail)
            # print(title)
            # print(rating)
            # print(created_date)
            # print(no)

            new_episode = Episode(
                # 크롤링한 결과를 에피소드 클래스의 뉴 에피소드 인스턴스로 생성
                # 에피소드 클래스에 인스턴스들을 만든것 (이 부분 이해가 안간다)
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )

            # episode_lists에 Episode인스턴스를 추가
            episode_lists.append(new_episode)
            # print(episode_lists)
            # 이 정보들을 넣고 새로운 인스턴스들을 만든다.

        return episode_lists

    # ep = episode_crawler(703845)
    # print(q)
    # for item in ep:
    #     print(item.no, item.title)

    def update(self):
        """
        update함수를 실행하면
        해당 웹툰 아이디에 따른 에피소드 정보들을 에피소드 인스턴스로 저장
        :return:
        """

        result = self.episode_crawler()
        # self.webtoon_id를 하는 이유는 해당 웹툰의 id(즉 내가 얻고 싶은 웹툰의 id)를 가져와야 하니까 -> self
        print(result)
        self.episode_list = result
        # 그렇게 받아온 result / 여기도 이해가 안간다....
        print(result)

# if __name__=='__main__' :
#     # 여기도 이해가 안가욤.....흑흑.....
#     webtoon2 = Webtoon(651673)
#     print(webtoon2.title)
#     webtoon2.update()
# # print(webtoon2.title)
#
#     for episode in webtoon2.episode_list:
#         print(episode.url)
