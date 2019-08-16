import requests
import re
import json


# def get_one_page(url):
#     """获取一页榜单信息"""
#     headers = {
#         'User - Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/69.0.3497.81 Safari/537.36'
#     }
#
#     response = requests.get(url, headers=headers)
#
#     if response.status_code == 200:
#         return response.text
#     return None
#
#
# def main():
#     url = 'https://maoyan.com/board/6?offset=0'
#     html = get_one_page(url)
#
#     # 匹配排名,利用 board-index 作为标志位
#     # parterns = '<dd>.*?board-index.*?>(\w+)</i>'
#
#     # result = re.findall(parterns, html, re.S)
#     #
#     # for items in result:
#     #     print(items)
#
#     # 匹配电影名,利用 name 作为标志位
#     # parterns = '<p.*?name.*?a.*?>(.*?)</a>'
#     #
#     # result = re.findall(parterns, html, re.S)
#     #
#     # for items in result:
#     #     print(items)
#
#     # 匹配图片资源,利用data-src 作为标志位
#     # parerns = 'data-src.*?"(.*?)"'
#     #
#     # result = re.findall(parerns, html, re.S)
#     #
#     # for items in result:
#     #     print(items)
#
#     # 匹配主演,利用 star 作为标志位
#     # parerns = 'star.*?>(.*?)</p>'
#     #
#     # result = re.findall(parerns, html, re.S)
#     #
#     # for items in result:
#     #     print(items)
#
#     # 匹配上映时间
#     # parerns = 'releasetime.*?>(.*?)</p>'
#     #
#     # result = re.findall(parerns, html, re.S)
#     #
#     # for items in result:
#     #     print(items)
#
#
#     # 整体 parerns
#     parerns = '<dd>.*?board-index.*?>(\w+)</i>.*?data-src.*?"(.*?)".*?<p.*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>'
#
#     result = re.findall(parerns, html, re.S)
#
#     print(result)
#
#     for items in result:
#         yield {
#             'index': items[0],
#             'image': items[1],
#             'name': items[2],
#             'star': items[3],
#             'releasetime': items[4]
#         }
#
#
#     # print(html)


# 改写 get_one_page 函数
def get_one_page(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/69.0.3497.81 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    return


def get_one_page_content(html):
    par = '<dd>.*?board-index.*?>(\w+)</i>.*?data-src.*?"(.*?)".*?<p.*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>'

    parerns = re.compile(par, re.S)

    result = re.findall(parerns, html)

    for items in result: yield {
            'index': items[0],
            'image': items[1],
            'name': items[2],
            'star': items[3],
            'releasetime': items[4]
        }

# 利用 format 将字典排序
# def write_to_file_by_format(content):
#     """构建字符串,使得字典里的元素以 index, name, image, star, releasetime 排序"""
#     result = []
#     for items in content:
#         item = "'index': {0[index]}, 'name': {0[name]}, 'image': {0[image]}, 'star': {0[star]}, 'releasetime': {0[releasetime]}\n".format(items)
#         # print(item)
#         result.append(item)
#
#     print(result)
#     with open('01-maoyan-TOP100.txt', 'a') as f:
#         f.writelines(result)


# 利用 JSON 将字典序列化
def write_to_file(content):
    with open('result.txt', 'at', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/6?offset=%d' % offset
    html = get_one_page(url)
    for item in get_one_page_content(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(5):
        main(i*10)
