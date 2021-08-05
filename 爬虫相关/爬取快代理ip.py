import  requests
from bs4 import  BeautifulSoup
from time import  sleep

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
class IPSpider:
    def __init__(self):
        self.page_urls = []
        for x in range(1,9):#爬取的页数
            print("正在爬取第{}页".format(x))
            page_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(x)
            self.page_urls.append(page_url)

    def parsr_page_url(self,url):
        resp = requests.get(url,headers = headers)
        html = resp.text
        soup = BeautifulSoup(html,'lxml')
        trs = soup.find('tbody').find_all('tr')
        infos = []
        for tr in trs:
            info = list(tr.stripped_strings)
            #info = ''.join(info)  #由于最后需要用到下标，所以还是列表形式即可，不用转成字符串形式
            infos.append(info)
        return infos

    def run(self):
        with open('ip.txt','w',encoding='utf-8') as f:
            f.write('{},{},{},{},{},{},{}\n'.format('IP\t', 'PORT\t', '匿名度\t', '类型\t', '位置\t', '响应速度\t', '最后验证时间\t'))
            for page_url in self.page_urls:
                #调用类中函数，函数前要加self
                print(page_url)
                sleep(1)
                infos = self.parsr_page_url(page_url)
                for info in infos:
                    #f.write('{},{},{},{},{},{},{}\n'.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6]))
                    f.write('{}:{}\n'.format(info[0],info[1]))


def main():
    spider = IPSpider()
    spider.run()

if __name__ == '__main__':
    main()

"""for ip in ip_list:
    
    try:
        response = requests.get(url='https://www.baidu.com', proxies=ip, timeout=2)
        if response.status_code == 200:
            use_proxy.append(ip)
    except Exception as e:
        print(f'当前为第{count}个代理ip:', ip, '请求超时, 检测不合格!!!')
    else:
        print(f'当前为第{count}个代理ip:', ip, '检测通过')"""




