"""
多线程包  threading
队列 包   queue
爬虫     requests
网页选择器    bs4
"""
import os
from threading import Thread
import queue
import requests
from bs4 import BeautifulSoup

# 1.创造请求头，模拟浏览器
headers = {
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}


# 2.编写一个爬虫类
class Reptile(Thread):
    # 重写构造方法
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        # 声明类属性
        self.url_queue = url_queue
        self.html_queue = html_queue

        # 创建视频存储文件夹
        if not os.path.exists("./video"):
            os.mkdir("./video")

    # 重写多线程中运行线程的函数
    def run(self):
        while not self.url_queue.empty():
            url = self.url_queue.get()
            response = requests.get(url, headers=headers)
            # 判断状态码
            if response.status_code == 200:
                self.html_queue.put(response.text)


# 3.解析爬取的数据
class Parse(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while not self.html_queue.empty():
            soup = BeautifulSoup(self.html_queue.get(), "lxml")
            videos_daat = soup.find_all("source")
            for video in videos_daat:
                src_url = video["src"]
                with open("./video/" + os.path.splitext(src_url)[0][31:] + os.path.splitext(src_url)[-1], "wb")as file:
                    data = requests.get("https:" + src_url, headers=headers).content
                    file.write(data)
                    print("下载完成：", os.path.splitext(src_url)[0][31:])


if __name__ == '__main__':
    # 创建队列
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    base_url = "https://www.qiushibaike.com/video/page/{}/"
    for page in range(1,6):
        new_url = base_url.format(page)
        url_queue.put(new_url)

    # 创建多线程爬虫任务
    reptile_list = []
    for i in range(3):
        reptile = Reptile(url_queue, html_queue)
        reptile_list.append(reptile)
        reptile.start()
    # 需要对线程对象调用join方法——等到其他任务完成后再退出
    for _ in reptile_list:
        _.join()

    parse_list = []
    for j in range(3):
        parse = Parse(html_queue)
        parse_list.append(parse)
        parse.start()
    for _ in parse_list:
        _.join()
