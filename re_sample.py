import re
# re_weekday_item_title.html파일을 불러와서 html변수에 할당
file_name = 'weekday.html'
with open('file_name', 'rt') as f:
    html = f.read()

# <a...class="title"...>[내용]</a>
# [내용] 에 해당하는 부분을 추출하는 정규표현식을 작성해서
# 실행한 결과 -> '유미의 세포들'이라고 나올 수 있도록

# <a...>[내용]</a>
# 1. <a로 시작해서
# 2. >가 등장하기 전까지의 임의의 문자 반복
# 3. >문자
# 4. <가 등장하기 전까지의 임의의 문자 반복을 그룹화
# 5. </a>문자
#p = re.compile(r'<a.*?>(.*?)</a>')

# 정규표현식 패턴 (a태그이며, class = "title"이 여는 태그에 포함되어 있을 경ㅇ, 내용부분을 그룹화)
p = re.compile(r'''<a                     # <a 로 시작하며
                   .*?class"title".*?>     # 중간에 class= "title"문자열이 존재하며 >가 등장하기 전까지의 임의의 문자 최소 반복, >까지
                   (.*?)                  # 임의의 문자 반복을 그룹화(findall 또는 finditer의 match objext에서 사용)
                   </a>                   # </a>가 나오기 전까지''', re.VERBOSE) #엔터와 공백은 다 무시가 됨
result = re.findall(p, html)
print(result)
