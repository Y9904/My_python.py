"""
唯品会————口红
动态数据
"""
import re
import csv
import requests

# 保存数据到CSV文件
file = open("唯品会——口红——商品信息.csv", "a", encoding="utf-8", newline="")
csv_writer=csv.DictWriter(file, fieldnames=["名称", "品牌", "售价", "原价", "折扣", "图片链接"])
csv_writer.writeheader()

def get_goods_data(pid):
    goods_url = "https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "referer": "https://category.vip.com/"
    }
    params_data = {
        "callback": "getMerchandiseDroplets1",
        "app_name": "shop_pc",
        "app_version": "4.0",
        "warehouse": "VIP_HZ",
        "fdc_area_id": "104102101",
        "client": "pc",
        "mobile_platform": "1",
        "province_id": "104102",
        "api_key": "70f71280d5d547b2a7bb370a529aeea1",
        "user_id": "",
        "mars_cid": "1614130805301_341a2eea8aca96af1d8706a5d8d2bd3c",
        "wap_consumer": "a",
        "productIds": "{}".format(pid),
        "scene": "search",
        "standby_id": "nature",
        'extParams': '{"stdSizeVids": "", "preheatTipsVer": "3", "couponVer": "v2", "exclusivePrice": "1", "iconSpec":"2x"}',
        "context": "",
        "_": "1614132009899"
    }
    resp = requests.get(goods_url, headers=headers, params=params_data)
    # 获取商品的具体信息
    title = re.findall('"title":"(.*?)"', resp.text, re.S)  # 名称
    brandShowName = re.findall('"brandShowName":"(.*?)"', resp.text, re.S)  # 品牌
    salePrice = re.findall('"salePrice":"(.*?)"', resp.text, re.S)  # 售价
    marketPrice = re.findall('"marketPrice":"(.*?)"', resp.text, re.S)  # 原价
    saleDiscount = re.findall('"saleDiscount":"(.*?)"', resp.text, re.S)  # 折扣
    squareImage = re.findall('"squareImage":"(.*?)"', resp.text, re.S)  # 图片
    goods_list = zip(title, brandShowName, salePrice, marketPrice, saleDiscount, squareImage)
    goods_dict={}
    for item in goods_list:
        goods_dict["名称"]=item[0]
        goods_dict["品牌"]=item[1]
        goods_dict["售价"]=item[2]
        goods_dict["原价"]=item[3]
        goods_dict["折扣"]=item[4]
        goods_dict["图片链接"]=item[5]
        print(goods_dict)
        csv_writer.writerow(goods_dict)

# 1.抓包找到能获取id值的url
url = "https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "referer": "https://category.vip.com/"
}
# 页数
for page in range(0, 10):
    params = {
        "callback": "getMerchandiseIds",
        "app_name": "shop_pc",
        "app_version": "4.0",
        "warehouse": "VIP_HZ",
        "fdc_area_id": "104102101",
        "client": "pc",
        "mobile_platform": "1",
        "province_id": "104102",
        "api_key": "70f71280d5d547b2a7bb370a529aeea1",
        "user_id": "",
        "mars_cid": "1614130805301_341a2eea8aca96af1d8706a5d8d2bd3c",
        "wap_consumer": "a",
        "standby_id": "nature",
        "keyword": "口红",
        "lv3CatIds": "",
        "lv2CatIds": "",
        "lv1CatIds": "",
        "brandStoreSns": "",
        "props": "",
        "priceMin": "",
        "priceMax": "",
        "vipService": "",
        "sort": "0",
        "pageOffset": "{}".format(page),
        "channelId": "1",
        "gPlatform": "PC",
        "batchSize": "120",
        "_": "1614132009897"
    }
    # 2.发送请求，获取每个商品的pid值
    response = requests.get(url, headers=headers, params=params)
    pid = re.findall('"pid":"(\d+)"', response.text, re.S)
    # 3.访问获取商品信息的函数
    pid_50=",".join(pid[:50])
    get_goods_data(pid_50)
    pid_100 = ",".join(pid[50:100])
    get_goods_data(pid_100)
    pid_120 = ",".join(pid[100:120])
    get_goods_data(pid_120)



