from cgitb import html
import random
import json
import asyncio
import aiohttp
import sys


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Cookie': '__jlcke__=; __jllaig__=1; __jltins__44072fce-0ba0-4d1d-bd57-8103a853f90a={"sid": 1649750218757, "vd": 2, "expires": 1649750825127}',
    'referer': 'https://w52zwzmmmkkk.xyz:52888/home/index.html'
}

def get_proxy():
    with open('C:\\Users\\13662\\Desktop\\python项目\\python爬虫\\爬色图\\欧美风情\\proxyPool.json', 'r') as f:
        proxyPool = json.load(f)
        prxylist = proxyPool['proxy']
    proxy = random.choice(prxylist)
    return proxy



# 使用代理池请求url；需要先开启ip池服务器，详见：https://github.com/jhao104/proxy_pool
async def request_url(url):
    retry_count = 5
    # 获取代理ip
    proxy = get_proxy()
    while retry_count > 0:
        try:
            #使用代理访问
            async with aiohttp.ClientSession() as session:
                async with session.get(url,  headers = headers) as response:
                    html = await response.text(encoding='utf-8')
                    return html
        except Exception:
            print('error connect')
            retry_count -= 1
    

loop = asyncio.get_event_loop()
loop.run_until_complete(request_url('https://w52zwzmmmkkk.xyz:52888/home/index.html'))