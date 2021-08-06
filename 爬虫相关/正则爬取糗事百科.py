import re
import  requests

def parse_page(url):
    headers = {
        'user - agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89Safari / 537.36'
    }
    response = requests.get(url,headers=headers)
    text = response.text
    # re.S = re.DOTALL
    #contents = re.findall(r"<div.+?>.*?<span>(.+?)</span>",text,re.DOTALL)  #正则表达式1
    contents = re.findall(r'<div\sclass="content">.*?<span>(.*?)</span>',text,re.DOTALL) #正则表达式2,\s表空白符
    duanzi = []
    for content in contents:
        #注意用re.sub()方法将标签替换成空字符串
        x = re.sub(r"<.+?>",'',content)
        #x = re.sub(r'<.*?>','',content)
        duanzi.append(x.strip())
        print(x.strip()) #去除空格
        print('='*50)


def main():
    url = 'https://www.qiushibaike.com/text/page/1/'
    for x in range(1,10):
        url = 'https://www.qiushibaike.com/text/page/%s/' % x
        parse_page(url)
        break

if __name__ == '__main__':
    main()