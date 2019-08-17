import requests
from pyquery import PyQuery as pq
import json



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

url = 'https://www.zhihu.com/hot'

response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    html = response.text
else:
    html = None

print(len(html))

doc = pq(html)
# doc = pq(filename='./test.html')

lists = doc('.HotItem')

title = lists.find('HotItem-title')
print(title)

content = doc('.HotItem-excerpt').items()

# for item in title:
#     print(item.text())
#
# for item in content:
#     print(item.text())

# print(type(title))
# print(title.text())













