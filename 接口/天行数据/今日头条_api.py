"""
天行数据
通过开放数据接口（数据集）获取数据
"""
import requests

key = "7d16b50b47854f861215777bff92137d"
response = requests.get(
    f"http://api.tianapi.com/topnews/index?key={key}"
)
data = response.json()
new_list = data["newslist"]
for new in new_list:
    print("-------------------------------------")
    ctime = new["ctime"]
    print("日期：", ctime)
    title = new["title"]
    print("标题：", title)
    description = new["description"]
    print("内容：", description)
    picUrl = new["picUrl"]
    print("图片url:", picUrl)
    url = new["url"]
    print("url:", url)
    source = new["source"]
    print("来源：", source)
