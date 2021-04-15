"""
爬取绝对领域中的异步加载的图片
"""
import os
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

#自动加载
def loading():
# 创建浏览器对象
    driver = webdriver.Chrome(executable_path="F:\python集\python01\自动化\浏览器驱动\chromedriver.exe")
    # 打开网站
    driver.get("https://www.jdlingyu.com/")

    # 自动加载  分页
    for i in range(2):
        # 点击加载更多
        loading = driver.find_element_by_xpath('//*[@id="primary-home"]/div[5]/div/div[1]/div/div[3]/button')
        loading.click()
        time.sleep(3)

    # 获取得到异步的渲染
    html = driver.page_source     #page_source 获取动态数据
    return html

# 获取图套的数据
def get_data():
    imgs=[]
    html=loading()
    # 数据解析
    data = BeautifulSoup(html, "lxml")
    first_data = data.find_all("ul", class_="b2_gap")[0]
    second_data=first_data.find_all("li")
    #每一个图套
    for message in second_data:
        imgs_data = message.find("h2")
        if imgs_data:
            href = imgs_data.find("a").attrs["href"]
            target = imgs_data.text
            imgs.append([target,href])
    return imgs

# 进入图套的详细页
def into_imgs():
    imgs=get_data()
    for img in imgs:
        target,url=img
        response=requests.get(url,headers=headers)
        response.endoing=response.apparent_encoding
        img_data=response.content
        html=BeautifulSoup(img_data,"lxml")
        data_1=html.find_all("div",class_="entry-content")[0]
        data_2=data_1.find_all("img")
        count=0
        for message in data_2:
            count+=1
            name=target+str(count)
            src=message["src"]
            data=requests.get(src,headers=headers).content
            save_imgs(target,name,data)


# 保存图片
def save_imgs(target,name, data):
    file="图集/{}".format(target)
    path = os.path.exists(file)
    if not path:
        os.makedirs(file)
    img_path = "图集/{}/{}.jpg".format(target, name)
    with open(img_path, "wb") as f:
        f.write(data)
    print("{}保存成功".format(name))
    # 休眠
    time.sleep(0.5)


if __name__ == '__main__':
    #请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    # get_data()
    into_imgs()
    print("全部保存完毕".center(50,"*"))