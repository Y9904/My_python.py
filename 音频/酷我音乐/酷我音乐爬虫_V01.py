import os
import requests
import json

# 创建保存音乐的文件夹
if not os.path.exists("./music"):
    os.mkdir("./music")

# 爬取网页内容
url = "https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%88%98%E7%8F%82%E7%9F%A3&pn=1&rn=30&httpsStatus=1&reqId=56ee8490-66e8-11eb-807a-af5f21e1975c"
# 1.发送请求与收到响应
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1612442711; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1612442711; _ga=GA1.2.1112277915.1612442711; _gid=GA1.2.924182503.1612442711; kw_token=A4SORW7D97",
    "csrf": "A4SORW7D97",
    "Host": "www.kuwo.cn",
    "Referer": "https://www.kuwo.cn/search/list?"
}

response = requests.get(url, headers=headers)

# 2.提取接受到的数据
data = response.json()["data"]["list"]
for message in data:
    name = message["name"]
    rid = message["rid"]

    # 抓包找到新的url
    new_url = "https://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1612445125104&httpsStatus=1&reqId=70859611-66ec-11eb-807a-af5f21e1975c".format(
        rid)
    music_data = requests.get(new_url)
    mp3_url = music_data.json()["url"]

    # 3.下载音乐
    mp3 = requests.get(mp3_url).content
    with open("./music/" + name + ".mp3", "wb")as file:
        file.write(mp3)
        print("下载完成：", name)
