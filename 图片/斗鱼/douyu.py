import os
import requests
from urllib import request
import threading

def douyu_image(page):
    '''
    :param page:  页码
    '''
    url=f'https://www.douyu.com/gapi/rknc/directory/yzRec/{page}'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
             }
    # 爬取本页信息
    response=requests.get(url,headers=headers).json()
    data=response['data']['rl']
    for i in data:
        name=i['nn']    #主播名称
        number=i['rid']   #主播房间号
        image=i['rs1']   #图片地址

        # 下载图片
        try:
            path=f'douyu_images/{page}-{name}-{number}.png'
            request.urlretrieve(image,path)
            print(f'正在下载{page}-{name}-{number}.png')
        except:
            print(f'error：{page}-{name}-{number}.png')


if __name__ == '__main__':
    # 保存路径
    if not os.path.exists('douyu_images'):
        os.mkdir('douyu_images')
    #多线程
    for i in range(1,5):
        t=threading.Thread(target=douyu_image,args=(i,))
        t.start()
