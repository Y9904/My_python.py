from concurrent.futures import ThreadPoolExecutor

import requests
import pprint
import os
import re



def file_name(name):
    new_name = re.sub(r'[\\\/\*\：\:\?\!\“\|\<\>]', '_', name)
    return new_name


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    # 发送请求 获取数据
    reponse = requests.get(url, headers=headers)
    return reponse


def get_video(page):
    url = f'https://v.6.cn/minivideo/getMiniVideoList.php?act=recommend&page={page}&pagesize=25'
    reponse = get_data(url)
    # 转换为js数据
    json_data = reponse.json()
    # 格式化输出js数据
    # pprint.pprint(json_data)
    # 解析数据
    data = json_data['content']['list']
    for message in data:
        # 房间号
        vid = message['vid']
        # 图片
        picurl = message['picurl']
        # 名称
        alias = message['alias']
        # 视频yul
        playurl = message['playurl']

        # 获取视频数据
        video = get_data(playurl).content
        # 文件名和路径
        new_name = file_name(alias)
        video_name = new_name + '.mp4'
        file_path = 'video/' + video_name
        print('正在下载：', video_name)
        # 保存本地
        with open(file_path, 'wb') as file:
            file.write(video)


if __name__ == '__main__':
    # 创建保存文件
    if not os.path.exists('video'):
        os.mkdir('video')
    # 页数
    page=[i for i in range(1,3)]
    with ThreadPoolExecutor(max_workers=6) as pool:
        pool.map(get_video,page)

