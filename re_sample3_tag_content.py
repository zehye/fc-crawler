# 전체 HTML 문서에서 '태그'를 찾고 해당 '태그'의 내용을 그룹화

# 1. < 로 시작하고
# 2. 사이에 임의의 문자열이 있으며( 태그명과 속성, 값 )
# 3. > 로 끝난 후
# 4. 임의의 문자열이 있거나 없을 수도 있다. ( 내용이 빈 태그 ) <- 그룹화
# 5. 다시 < 를 만난 후
# 6. 사이에 임의의 문자열이 있으며
# 7. > 로 끝나는 경우
# 모든 경우는 최소반복
import re

# []는 제외하고 라는 의미
p = re.compile(r'<[^/]*?>(.*?)</.*?>', re.DOTALL)
html = open('re_tag_content_example.html', 'rt').read()

result = re.findall(p, html)
for item in result:
    print(item)
