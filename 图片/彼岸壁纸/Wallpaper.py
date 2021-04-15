import os

import requests
from bs4 import BeautifulSoup


# 1.选择壁纸风格
def choice_style():
    # 操作的菜单目录
    print("壁纸风格".center(50, "="))
    print("1.风景壁纸".center(50, " "))
    print("2.美女壁纸".center(50, " "))
    print("3.游戏壁纸".center(50, " "))
    print("4.动漫壁纸".center(50, " "))
    print("5.动物壁纸".center(50, " "))
    print("6.美食壁纸".center(50, " "))
    print("".center(54, "="))
    # 选择壁纸的风格
    choice = input("请选择壁纸风格:")
    url_list = []
    if choice == "1":
        url = "http://pic.netbian.com/4kfengjing/"
        url_list.append("风景壁纸")
        url_list.append(url)
    elif choice == "2":
        url = "http://pic.netbian.com/4kmeinv/"
        url_list.append("美女壁纸")
        url_list.append(url)
    elif choice == "3":
        url = "http://pic.netbian.com/4kyouxi/"
        url_list.append("游戏壁纸")
        url_list.append(url)
    elif choice == "4":
        url = "http://pic.netbian.com/4kdongman/"
        url_list.append("动漫壁纸")
        url_list.append(url)
    elif choice == "5":
        url = "http://pic.netbian.com/4kdongwu/"
        url_list.append("动物壁纸")
        url_list.append(url)
    elif choice == "6":
        url = "http://pic.netbian.com/4kmeishi/"
        url_list.append("美食壁纸")
        url_list.append(url)
    else:
        print("输入有误，请重新输入！")
    return url_list


# 2、获取壁纸信息
def get_img():
    # 壁纸的页数
    style, choice_url = choice_style()
    for i in range(2, 12):
        url = choice_url + "index_{}.html".format(i)
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        data = response.text
        # 解析数据
        html = BeautifulSoup(data, "lxml")
        imgs_data = html.find_all("ul", class_="clearfix")[0]
        imgs_msg = imgs_data.find_all("li")
        for message in imgs_msg:
            # 获取壁纸名称
            title = message.find("b").text
            # 获取壁纸的url
            img_url = base_url + message.find("img")["src"]
            # 保存
            img = requests.get(url=img_url, headers=headers).content
            save_file(style, title, img)


# 3.保存壁纸
def save_file(style, title, data):
    path = os.path.exists(style)
    if not path:
        os.mkdir(style)
    img_path = "{}/{}.jpg".format(style, title)
    with open(img_path, "wb") as f:
        f.write(data)
    print("{}   保存成功".format(title))


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    base_url = "http://pic.netbian.com"

    get_img()
