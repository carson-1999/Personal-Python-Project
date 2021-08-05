import requests
from bs4 import BeautifulSoup
from time import sleep

headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Host': 'www.kuaidaili.com',}
    

#存储各个未测试的ip
infos = []


def parse_page_url(url):
    try:
        resp = requests.get(url, headers=headers)
        html = resp.text
        print(resp.status_code)
        soup = BeautifulSoup(html, 'lxml')
        #trs = soup.find('tbody').find_all('tr')
        trs = soup.find('tbody').find_all('tr')
        for tr in trs:
            info = list(tr.stripped_strings)
            ip = info[0]
            port = info[1]
            ip = ip+":"+port
            # info = ''.join(info)  #由于最后需要用到下标，所以还是列表形式即可，不用转成字符串形式
            infos.append(ip)
    except Exception:
        pass


for x in range(1, 60):
    print("爬取第"+str(x)+"页的ip")
    url = 'https://www.kuaidaili.com/free/inha/{}/'.format(x)
    print(url)
    parse_page_url(url)


use_proxy = []  # 检测通过的可用ip
count = 0
for ip in infos:
    try:
        count += 1
        response = requests.get(
            url='https://www.baidu.com', proxies=ip, timeout=5)
        if response.status_code == 200:
            use_proxy.append(ip)
    except Exception as e:
        print(f'当前为第{count}个代理ip:', ip, '请求超时, 检测不合格!!!')
    else:
        print(f'当前为第{count}个代理ip:', ip, '检测通过')

print("可用的ip列表:", use_proxy)
