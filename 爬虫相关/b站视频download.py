import time
import requests
from  bs4 import BeautifulSoup
from requests import RequestException
import re
import json
import urllib
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


class BilibiliSpider:
    def __init__(self,bv):
        #视频页地址
        self.url = 'https://www.bilibili.com/video/' + bv
        #开始时间
        self.start_time = time.time()


    def get_video_info(self):
        try:
            resp = requests.get(self.url, headers=headers)
            # 假如请求成功
            if resp.status_code == 200:
                #创建BS4对象
                soup = BeautifulSoup(resp.text, 'lxml')
                # 获取视频标题
                video_title = soup.find('span', class_='tit tr-fix').get_text()
                # 获取视频url
                pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL) #事先编译正则匹配模式
                script = soup.find("script", text=pattern) #找到text文本内容为前面编译规则的script标签，且find返回这个标签
                # 注意script是返回包括标签名的整个标签，而script.next是去掉前后的标签名，就剩下标签里的内容，再用group(1)提取出分组
                #而前面事先编译了正则的匹配模式，再配合search()方法，参数是标签内容作为匹配的搜索文本
                result = pattern.search(script.next).group(1) #后面的group(1)提取出了内容后面的分组，即包含着字典的字符串
                #而json对象本质上就是个字符串，利用json.loads()函数转化为python的字典对象，方便后面根据key提取值
                temp = json.loads(result) #json对象转化为python字典对象
                print(temp)
                # 取第一个视频链接,baseUrl存在于字典中的data中的dash中的video
                for item in temp['data']['dash']['video']:
                    if 'baseUrl' in item.keys():  #判断下baseurl的键值是否存在再进行提取baseurl
                        video_url = item['baseUrl']
                        break
                #函数返回字典对象
                return {
                    'title': video_title, #返回标题
                    'url': video_url    #返回url
                }
        except requests.RequestException:  #俘获异常
            print('视频链接错误，请重新更换')

    def download_video(self, video):
        # 获取前面函数获取的视频标题并运用re模块对视频标题中括号中特定字符串的替换成-。
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        #获取前面函数获取的视频url
        url = video['url']
        #给定下载的视频的文件名
        filename = title + '.mp4'
        #利用urllib.request创建一个opener对象
        opener = urllib.request.build_opener()
        #增加opener请求头对象，圆括号形式，多个则需要列表包括
        opener.addheaders = [('Origin', 'https://www.bilibili.com'),
                             ('Referer', self.url),
                             ('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url = url, filename = filename, reporthook = self.schedule)

    def schedule(self, blocknum, blocksize, totalsize):
        '''
        urllib.urlretrieve 的回调函数
        :param blocknum: 已经下载的数据块
        :param blocksize: 数据块的大小
        :param totalsize: 远程文件的大小
        :return:
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        #round()方法是四舍五入，后面没参数则是对整数的四舍五入，ljust()方法是返回左对齐，前面参数是数量，后面是填充的具体字符
        s = ('#' * round(percent)).ljust(100, '-')
        #下面是对进度条输出样式的设计
        sys.stdout.write("%.2f%%" % percent + '[ ' + s + ']' + '\r')
        #下面这句是为了刷新输出
        sys.stdout.flush()


def main():
    #传入下载视频url的后缀
    video_last = input('请输入你要下载的b站视频的url的video的后缀: ')
    spider = BilibiliSpider(video_last)
    video = spider.get_video_info()
    spider.download_video(video)

if __name__ == '__main__':
    main()