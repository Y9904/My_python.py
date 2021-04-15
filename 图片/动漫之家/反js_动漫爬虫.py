"""
思路：
1、获取所有的章节名称和章节的链接
2、根据章节链接获取章节里面图片的链接
3、根据章节名保存漫画图片
"""
import requests
from bs4 import BeautifulSoup
import re
import os
import time


def change_title(title):
    """处理文件名非法字符的方法"""
    pattern = re.compile(r'[/:*?"<>|\\]')  # / \ : * ? < > |
    new_title = re.sub(pattern, "_", title)
    return new_title


# 1、获取所有的章节名称和章节的链接(静态加载)
# 目标网址
url = "https://www.dmzj.com/info/yaoshenji.html"
headers = {"Referer": "https://www.dmzj.com/",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
           }

# 获取数据
response = requests.get(url).text
# 解析数据
soup = BeautifulSoup(response, "lxml")
# 提取数据
list_con_li = soup.find("ul", class_="list_con_li autoHeight")
chapter_data = list_con_li.find_all("a")
# 章节名
chapter_names = []
# 章节链接
chapter_urls = []
for chapter in chapter_data:
    name = chapter.text
    href = chapter["href"]
    if "." in name:
        name_1 = name.replace(".", " ")
        chapter_names.insert(0, name_1)
    else:
        chapter_names.insert(0, name)
        chapter_urls.insert(0, href)

# 2、根据章节链接获取章节里面图片的链接（动态加载）
# 动态加载———— javascript
# 1.外部加载
# 2.内部加载
for i, url in enumerate(chapter_urls):
    data = requests.get(url).text
    html = BeautifulSoup(data, "lxml")
    script_data = html.script  # 获取  js 文本
    message = re.findall("\|(\d{13,14})\|", str(script_data))
    for j, number in enumerate(message):
        if len(number) == 13:
            message[j] = number + "0"
    pics = sorted(message, key=lambda x: int(x))  # 比较大小，进行排序
    message_1 = re.findall("\|(\d{4})\|", str(script_data))[0]
    message_2 = re.findall("\|(\d{5})\|", str(script_data))[0]
    # 构造图片地址
    for k, pic in enumerate(pics):
        if pic[-1] == "0":
            url = "https://images.dmzj1.com/img/chapterpic/" + message_1 + "/" + message_2 + "/" + pic[:-1] + ".jpg"
        else:
            url = "https://images.dmzj1.com/img/chapterpic/" + message_1 + "/" + message_2 + "/" + pic + ".jpg"

        # 3、根据章节名保存漫画图片
        pic_name = "%03d.jpg" % (k + 1)
        chapter_name = chapter_names[i]
        new_name = change_title(chapter_name)
        # 创建保存文件夹
        book_name = "妖神记"
        if not os.path.exists(book_name):
            os.mkdir(book_name)
        path = os.path.join(book_name, new_name)
        if not os.path.exists(path):
            os.mkdir(path)
        pic_data = requests.get(url, headers=headers)
        try:
            with open(path + "/" + pic_name, "wb")as file:
                file.write(pic_data.content)
        except:
            pass
    print("正在下载：", chapter_names[i])
    time.sleep(0.5)
