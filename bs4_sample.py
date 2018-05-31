# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">...</p>
# """
#
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'lxml')
#
# #print(html_doc)
# #print(soup.prettify())
# #
# # print(soup.title)
# # print(soup.title.name)
# # print(soup.title.string)
# # print(soup.title.parent.name) # title태그의 부모요소의 이름까지도 출력
# # print(soup.title.parent)
# # print(soup.p) # 첫번째 p만 찾아준다.
# # print(soup.find_all('p')) # 전체 p를 다 찾아준다.
#
# for anchor in soup.find_all('a'):
#     print(anchor.get('href'))

#
from bs4 import BeautifulSoup
html = open('data/weekday.html', 'rt').read()
soup = BeautifulSoup(html_doc, 'lxml')

div_content = soup.find('div', id='content')
div_list_area = div_content.find('div', class_='list_area')
div_col_list = div_list_area.find_all('div', class_='col')

for col in div_col_list:
    print(col)


soup.select('a.title') # 여러개
for a in a_list:
    print(a.get