import requests
from random import choice, randint
from lxml import etree
import os
# 多线程
from concurrent.futures import ThreadPoolExecutor
from time import sleep

# 自己构造请求头池  用于切换请求头
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 不存在文件夹  就创建
if not os.path.exists('套图'):
    os.mkdir('套图')


# 获取5页的套图的URL
def get_taotu_url():
    taotu_urls = []
    for i in range(1, 6):
        url = f'http://www.win4000.com/wallpaper_209_0_0_{i}.html'
        headers = {
            'User-Agent': choice(user_agent)
        }
        # 发送请求  获取响应
        rep = requests.get(url, headers=headers)
        # 解析数据
        html = etree.HTML(rep.text)
        taotu_url = html.xpath('//div[@class="tab_tj"]/div/div/ul/li/a/@href')
        # 一个页面有24个图片
        taotu_urls.extend(taotu_url)
    return taotu_urls


# 进入套图详情页爬取图片
def get_img(url):
    headers = {
        'User-Agent': choice(user_agent)
    }
    # 发送请求  获取响应
    rep = requests.get(url, headers=headers)
    # 解析响应
    html = etree.HTML(rep.text)
    # 获取套图名称
    name = html.xpath('//div[@class="ptitle"]/h1/text()')[0]
    path = r'./套图/{}'.format(name)
    if not os.path.exists(path):
        os.mkdir(path)
    # 获取套图里的图片页数
    pic_number = html.xpath('//div[@class="pic_main"]/div/div[1]/div[1]/em/text()')[0]
    # 构造图片的url
    pic_url = url.replace(".html", "_{}.html")
    for i in range(1, int(pic_number)):
        # 休眠
        sleep(randint(1, 3))
        # 发送请求  获取响应
        reps = requests.get(pic_url.format(i), headers=headers)
        # 解析响应
        dom = etree.HTML(reps.text)
        # 提取图片下载链接
        src = dom.xpath('//div[@class="main-wrap"]/div[1]/a/img/@src')[0]
        # 构造图片保存的名称
        file_name = name + f'第{i}张.jpg'
        # 请求下载图片  保存图片  输出提示信息
        img = requests.get(src, headers=headers).content
        with open(r'./套图/{}/{}'.format(name, file_name), 'ab') as f:
            f.write(img)
            print(f'成功下载图片：{file_name}')


# 主函数调用  开多线程
def main():
    taotu_urls = get_taotu_url()
    with ThreadPoolExecutor(max_workers=4) as exector:
        exector.map(get_img, taotu_urls)
    print('=================== 图片全部下载成功啦！ =====================')


if __name__ == '__main__':
    main()
