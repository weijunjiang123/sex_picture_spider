import requests
import json

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

proxyPool = []
for _ in range(50):
    proxy = get_proxy().get("proxy")
    proxyPool.append(proxy)
proxydict = {
    'proxy':proxyPool
}
proxyjson = json.dumps(proxydict)
with open('proxyPool.json', 'w') as f:
    f.write(proxyjson)
    