'''
有道翻译_js逆向
url=https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
post请求
form data:
i: 你好                                    变化
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 16183136332691
sign: ae6dece954f5780836c4d53c95fd59ae    变化
lts: 1618313633269                        变化
bv: 3d48d980eaf4d7f3163f7987bd8bc39a      变化
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
'''
import execjs
import requests
import pprint    #格式化输出模块


while True:
    # 判断是否退出
    word=input('请输入原文(空值退出)：')
    if not word:
        break

    # 1.使用python代码调用js代码
    with open('js_解密.js', 'r', encoding='utf-8') as file:
        js_data = file.read()
    #调用js函数
    js_message = execjs.compile(js_data)
    sign = js_message.call('youdao', word)


    #2.向有道翻译发送请求
    youdao_url='https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Referer': 'https://fanyi.youdao.com/',
        'Origin': 'https://fanyi.youdao.com',
        'Host': 'fanyi.youdao.com',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-355630090@10.108.160.100; JSESSIONID=aaaqq_IDv6QtLcYAHalJx; OUTFOX_SEARCH_USER_ID_NCOO=384227200.94670206; ___rl__test__cookies=1618317989979',
        'X-Requested-With':'XMLHttpRequest'
    }
    data= {
        'i':word,
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':sign['salt'],
        'sign':sign['sign'],
        'lts':sign['ts'],
        'bv':sign['bv'],
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTlME'
    }
    response=requests.post(url=youdao_url,data=data,headers=headers).json()
    # pprint.pprint(response)

    #3.解析数据
    data=response['translateResult'][0][0]
    scr=data['src']
    tgt=data['tgt']
    print('译文：',tgt)
