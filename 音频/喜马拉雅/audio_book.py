"""
喜马拉雅————中国民间故事
"""
import os
import re
import requests
import parsel


def change_title(title):
    """处理文件名非法字符的方法"""
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")  # / \ : * ? < > |
    new_title = re.sub(pattern, "_", title)
    return new_title


# 翻页
for page in range(1, 5):
    print("----------------正在爬取{}页的数据---------------".format(page))
    url = "https://www.ximalaya.com/youshengshu/4256765/p{}/".format(page)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    # 1.发送请求
    response = requests.get(url, headers=headers)
    # 2.解码
    response.encoding = response.apparent_encoding
    # 3.解析数据    解析音频的 id值
    html_data = parsel.Selector(response.text)
    li_data = html_data.xpath("//div[@class='sound-list _is']/ul/li")

    for li in li_data:
        try:
            title = li.xpath(".//a/@title").get()
            href = li.xpath(".//a/@href").get()
            id_number = href.split("/")[-1]

            # 4.发送包含 id值 的url  获取json数据
            json_url = f"https://www.ximalaya.com/revision/play/v1/audio?id={id_number}&ptype=1"
            json_data = requests.get(url=json_url, headers=headers).json()
            # 5.提取json数据中音频地址
            m4a_url = json_data["data"]["src"]
            # 6.请求音频地址，获取音频数据
            m4a_data = requests.get(url=m4a_url, headers=headers).content

            # 修改名称
            new_title = change_title(title)
            # 7.数据持久化（保存）
            if not os.path.exists("中国民间故事"):
                os.mkdir("中国民间故事")
            path = "中国民间故事\\" + new_title + ".m4a"
            with open(path, "wb")as file:
                file.write(m4a_data)
                print("保存完成：", new_title)
        except:
            pass
