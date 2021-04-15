import requests
import re
import os

chapters_url = "https://www.qb5.tw/book_17934/"

# 获取小说目录页全部内容
response = requests.get(url=chapters_url)
response.encoding = response.apparent_encoding
html_data = response.text

# 获取书名
book_name = re.findall('<h1>(.*?)<small>/.*?</small></h1>', html_data, re.S)[0].strip()

# 创建保存所需的文件夹
path = os.path.exists(".\{}".format(book_name))
if not path:
    os.mkdir(book_name)

# 获取所有章节的url
chapters_list = re.findall('<dd><a href="(.*?)">.*?</a></dd>', html_data, re.S)

# 获取每一章内容
for url in chapters_list:
    # 构建完整的url
    text_url = chapters_url + url
    text_data = requests.get(text_url)
    text_data.encoding = text_data.apparent_encoding
    book_text = text_data.text

    # 目录名
    chapter_name=re.findall('<h1>(.*?)</h1>',book_text,re.S)[0]
    # 正文
    stroy = re.findall('<div id="content">.*?<br><br>(.*?)</div>', book_text, re.S)[0].replace("&nbsp;", "").replace("<br />", "")

    # 保存到本地文件夹
    try:
        print("正在保存{}".format(chapter_name))
        book_path=f"./{book_name}/{chapter_name}.txt"
        with open(book_path, "w", encoding="gkb") as file:
            file.write(stroy)
    except:
        print("{}保存失败".format(chapter_name))


print("*****************保存完成*****************")
