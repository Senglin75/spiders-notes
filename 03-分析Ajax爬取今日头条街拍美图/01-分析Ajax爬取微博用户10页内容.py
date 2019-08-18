from pyquery import PyQuery as pq
import requests, json
from urllib.parse import urlencode


def get_one_page(page):
    """获取微博一页内容"""
    base_url = 'https://m.weibo.cn/api/container/getIndex?'

    headers = {
        'Referer': 'https://m.weibo.cn/u/2830678474',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }

    parmas = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }

    url = base_url + urlencode(parmas)

    response = requests.get(url, headers=headers)

    return response.json() if response.status_code == 200 else None

    # print(json)


def parse_one_page(json_content):
    """从一页微博内容中解析出 id, 正文, 点赞数, 评论"""
    if json_content:
        items = json_content.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes_count'] = item.get('attitudes_count')
            weibo['comment_count'] = item.get('comments_count')
            # 将解析出来的 weibo 字典返回
            yield weibo


def main(page):
    json_content = get_one_page(page)
    results = parse_one_page(json_content)

    for result in results:
        with open('results.txt', 'a', encoding='utf8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    for i in range(1, 10):
        main(i)









