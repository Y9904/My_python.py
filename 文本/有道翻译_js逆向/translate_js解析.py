'''
有道翻译_js逆向
url=https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
post请求
form data:
i: 你好                                    变化      翻译原文
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 16183136332691                      变化        13位时间戳  + 一位时间戳
sign: ae6dece954f5780836c4d53c95fd59ae    变化        "fanyideskweb" + 翻译原文 + salt + "Tbh5E8=q6U3EXe+&L[4c@" 经过md5加密
lts: 1618313633269                        变化        13位时间戳
bv: 3d48d980eaf4d7f3163f7987bd8bc39a      不变化        请求头经过 md5 加密后字符串
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
'''
import requests
import random
import time
import hashlib

while True:
    # 判断是否退出
    word = input('请输入原文(空值退出)：')
    if not word:
        break

    # 通过js解密后得到 变化的参数
    lts = str(int(time.time() * 1000))
    salt = lts + str(random.randint(0, 9))
    # md5加密  得到sign参数
    str_data = "fanyideskweb" + word + salt + "Tbh5E8=q6U3EXe+&L[4c@"
    md5 = hashlib.md5()
    md5.update(str_data.encode('utf-8'))
    sign = md5.hexdigest()

    # 2.向有道翻译发送请求
    youdao_url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Referer': 'https://fanyi.youdao.com/',
        'Origin': 'https://fanyi.youdao.com',
        'Host': 'fanyi.youdao.com',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-355630090@10.108.160.100; JSESSIONID=aaaqq_IDv6QtLcYAHalJx; OUTFOX_SEARCH_USER_ID_NCOO=384227200.94670206; ___rl__test__cookies=1618317989979',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': '3d48d980eaf4d7f3163f7987bd8bc39a',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    response = requests.post(url=youdao_url, data=data, headers=headers).json()

    # 3.解析数据
    data = response['translateResult'][0][0]
    scr = data['src']
    tgt = data['tgt']
    print('译文：', tgt)
