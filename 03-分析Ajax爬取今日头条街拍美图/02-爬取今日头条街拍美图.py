from hashlib import md5
from urllib import parse
from multiprocessing import Pool
import requests
import os
import re


def get_one_page(offset):
    """获取头条街拍一页图片"""
    base_url = 'https://www.toutiao.com/api/search/content/?'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        # 必须添加 cookie 否则会被认定为 爬虫,无法爬取
        'cookie': 'tt_webid=6726379622944294412; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6726379622944294412; csrftoken=e175b2a321ee164be51d9519003abd61; s_v_web_id=bc4001f1f54ad18098f9efbd3a95fb32; __tasessionId=ajvtrdyig1566143159275'
    }
    parmas = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        # 取出返回的视频结果
        'has_video': 'false'
    }

    url = base_url + parse.urlencode(parmas)

    try:
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else None
    except requests.ConnectionError as e:
        return None


def get_images(json_content):
    """获取图片的 url"""
    if json_content:
        data = json_content.get('data')  # list 内嵌套字典
        for item in data:
            if item.get('title') is None:
                continue
            # title = re.sub('[\t]', '', item.get('title'))
            title = item.get('title')
            images = item.get('image_list')
            if images is None:
                continue
            for image in images:
                # 比较缩略图和大图之间的 url 差别,发现大图没有尺寸 190x124 并且 list 改为 large
                # print(image.get('url'))
                # print(re.sub('/list.*?/tos', '/large/tos', image.get('url')))
                yield {
                    'title': title,
                    'url': re.sub('/list.*?/tos', '/large/tos', image.get('url'))
                }


def save_images(images):
    """以图片名作为文件夹名字,保存图片至本地"""
    if images:
        folder = 'image/' + images.get('title')
        if not os.path.exists(folder):
            os.makedirs(folder)
            try:
                response = requests.get(images.get('url'))
                if response.status_code == 200:
                    # 利用图片内容的 MD5 值作为文件名,避免与文件夹名重复
                    file_path = '{folder}/{file}.{suffix}'.format(folder=folder,
                                                                  file=md5(response.content).hexdigest(),
                                                                  suffix='jpg')
                    if not os.path.exists(file_path):
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                            print('Downloading image: ', file_path)
                    else:
                        print('Already Downloaded', file_path)
            except Exception as e:
                print('Failed to save image')


def parse_page(offset):
    json_content = get_one_page(offset)
    images = get_images(json_content)
    if images is not None:
        for image in images:
            save_images(image)


GROUP_START = 0
GROUP_END = 10


def main():
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END)])
    pool.map(parse_page, groups)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()








