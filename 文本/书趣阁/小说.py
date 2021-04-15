import os
import re
from concurrent.futures import ThreadPoolExecutor
import requests


def get_data(url):
    '''
    获取网页数据
    :param url: 网页地址
    :return: 网页数据
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Referer': 'http: // www.shuquge.com / txt / 63542 / index.html',
        'Host': 'www.shuquge.com'
    }
    response = requests.get(url, headers=headers)
    return response


def text_urls(content_url):
    '''
    获取所有章节的url
    :return:
    '''
    reponse = get_data(content_url)
    # 转码
    reponse.encoding = reponse.apparent_encoding
    content_text = reponse.text
    # 获取所有章节的url
    text_url_list = re.findall(r'<dd><a href="(.*?)">.*?</a></dd>', content_text, re.S)
    # 清洗数据，去掉重复的url
    urls = []
    for i in text_url_list:
        if i not in urls:
            urls.append(i)
    return urls


def get_text(id_number):
    url = 'http://www.shuquge.com/txt/63542/'+id_number
    reponse = get_data(url)
    # 转码
    reponse.encoding = reponse.apparent_encoding
    text_data = reponse.text
    # 章节名
    text_name = re.findall('<h1>(.*?)</h1>', text_data, re.S)[0]
    name = file_name(text_name)
    print(f'正在保存{name}')
    # 正文内容
    text = re.findall(r'<div id="content" class="showtxt">(.*?)</div>', text_data, re.S)[0]
    data = text.replace('&nbsp;', '').replace('<br/>', '').replace('<br />', '')
    # 保存正文内容
    text_path = book_name+'/' + name + '.txt'
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(data)


def file_name(name):
    '''
    去掉文件名中不能包含的字符
    :param name:
    :return:
    '''
    new_name = re.sub('[/\\\?:*!“<>|]', '', name)
    return new_name


def pool(content_url):
    '''
    创建线程池
    :return:
    '''
    urls = text_urls(content_url)
    #线程池
    with ThreadPoolExecutor(max_workers=6) as Pool:
        Pool.map(get_text, urls)


if __name__ == '__main__':
    # 目录页的url
    content_url = 'http://www.shuquge.com/txt/63542/index.html'
    #书名
    book_name='三寸人间'
    # 创建保存文件
    if not os.path.exists(book_name):
        os.mkdir(book_name)
    pool(content_url)
