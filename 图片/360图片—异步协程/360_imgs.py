import os

import aiohttp  # 异步请求
import requests
import asyncio  # 异步协程
import aiofile  # 异步文件

HD = {
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.183Safari / 537.36"
}


async def download_picture(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HD,ssl=False) as response:
            data = await response.read()
            filename = url.split('/')[-1]
            path = f'images/{filename}'
            with open(path, 'wb') as file:
                file.write(data)


def main():
    loop = asyncio.get_event_loop()
    for num in range(1, 6):
        resp = requests.get(f'https://image.so.com/zjl?ch=beauty&sn={num * 30}', headers=HD)
        data_dict = resp.json()
        cos_list = []
        for beauty_dict in data_dict['list']:
            picture_url = beauty_dict['qhimg_url']
            cos_list.append(download_picture(picture_url))
        loop.run_until_complete(asyncio.wait(cos_list))
    loop.close()


if __name__ == '__main__':
    if not os.path.exists('images'):
        os.mkdir('images')
    main()
