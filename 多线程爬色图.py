import os
import random
import json
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import warnings
import time
import multiprocessing
warnings.filterwarnings('ignore')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Cookie': '__jlcke__=; __jllaig__=1; __jltins__44072fce-0ba0-4d1d-bd57-8103a853f90a={"sid": 1649750218757, "vd": 2, "expires": 1649750825127}',
    'referer': 'https://w52zwzmmmkkk.xyz:52888/home/index.html'
}


def get_proxy():
    with open('proxyPool.json', 'r') as f:
        proxyPool = json.load(f)
        prxylist = proxyPool['proxy']
    proxy = random.choice(prxylist)
    return proxy



# 使用代理池请求url；需要先开启ip池服务器，详见：https://github.com/jhao104/proxy_pool
def request_url(url):
    retry_count = 5
    # 获取代理ip
    proxy = get_proxy()
    while retry_count > 0:
        try:
            #使用代理访问
            r = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers = headers, verify=False)
            r.encoding = 'utf-8'
            return r.text
        except Exception:
            retry_count -= 1

    return None

# 获取当图片集的url链接，返回url列表
def get_page_urls():
    for i in range(1, 2):
        url = 'https://w52zwzmmmkkk.xyz:52888/home/piclist/7/829-' + str(i) + '.html'
        html = request_url(url)
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.find(class_='vodlist piclist').find_all(class_='listpic')
        urls = []
        for element in elements:
            pic_link = element.find('a').get('href')
            pic_link = 'https://q52zqzccceee.xyz:52888' + pic_link
            print('图片链接： %s' % pic_link)
            urls.append(pic_link)
    return urls

# 下载单个图片
def download_pic(title, image_list):
    os.mkdir(title)
    j = 1
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print("downloading ... %s ----> NO.%s" % (filename, str(j)))
        with open(filename, 'wb') as f:
            proxy = get_proxy()
            try:
                img = requests.get(item, proxies={"http": "http://{}".format(proxy)}, headers=headers, verify=False).content
                f.write(img)
                time.sleep(2)
            except:
                print(f"{filename} 下载失败")
                time.sleep(5)
        j = j + 1

# 从get_page_urls()获取的url下载图片集，调用download_pic()下载单个图片
def download(url):
    html = request_url(url)
    soup = BeautifulSoup(html)
    title = soup.find(class_='newsbody').find(class_='title').string
    total = soup.find(class_='nbodys').find_all('img')
    image_list = []
    for item in total:
        pic_link = item.get('src')
        image_list.append(pic_link)
    download_pic(title, image_list)

# 传入图片集url列表，调用download（），多进程下载图片集
def download_all_images(list_page_urls):
    # 获取每一个详情妹纸
    # works = len(list_page_urls)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(download, list_page_urls)
    pool.close()
    pool.join()

if __name__ == '__main__':
    # 获取每一页的链接和名称
    list_page_urls = get_page_urls()
    download_all_images(list_page_urls)
