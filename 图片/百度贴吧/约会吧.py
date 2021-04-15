"""
百度贴吧————约会吧
"""
import os

import requests
import parsel

# 翻页
for page in range(0,5):
    print(f"------------------------第{page+1}页---------------------------------")
    url = f"https://tieba.baidu.com/f?kw=%E7%BA%A6%E4%BC%9A&ie=utf-8&pn={50*page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; W0W64; Trident/7.0; rv:11.0) like Gecko"
    }
    # 1.发送请求
    response = requests.get(url=url, headers=headers)
    # 2.解析数据
    html = parsel.Selector(response.text)  # 转换数据格式-----xpath
    # 3.提取href
    href_list = html.xpath("//div[@class='threadlist_lz clearfix']/div/a/@href").getall()
    # 4.构建完整的url
    for href in href_list:
        title_url = "https://tieba.baidu.com" + href
        print("当前帖子链接：",title_url)
        # 5.继续发送请求，获取详情页数据
        resp = requests.get(url=title_url, headers=headers)
        # 6.二次解析数据
        imgs_data = parsel.Selector(resp.text)
        # 7.提取图片url
        imgs_src = imgs_data.xpath('//cc/div/img[@class="BDE_Image"]/@src').getall()
        # 8.请求图片的url
        for img_url in imgs_src:
            img=requests.get(img_url).content
            #图片名称
            img_name = img_url.split("/")[-1]
            # 9.保存图片
            file_name="约会吧——图片"
            if not os.path.exists(file_name):
                os.mkdir(file_name)
            path=file_name+"\\"+img_name
            with open(path,"wb")as file:
                file.write(img)
                print("保存完成：",img_name)
