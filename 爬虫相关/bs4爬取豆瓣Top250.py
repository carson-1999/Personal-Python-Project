import requests
from bs4 import  BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

}

"""获取详情页面的urls"""
def get_detail_urls(url):
    resp = requests.get(url, headers=headers)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')  # 创建一个beautifulsoup对象
    list = soup.find('ol', class_="grid_view").find_all('li')  # 注意class是关键字，用class_才行
    detail_urls = []
    for li in list:
        detail_url = li.find('a')['href']
        detail_urls.append(detail_url)
    return detail_urls

"""解析详情页面的内容并保存数据"""
def parse_detail_url(detail_urls,f):
    for detail_url in detail_urls:
        resp = requests.get(detail_url,headers = headers)
        html = resp.text
        soup = BeautifulSoup(html,'lxml')
        #获取电影名方式一（get_text())
        #name = soup.find('div',id='content').find('h1').get_text()
        #print(name)
        #获取电影名方式二,stripped_strings,注意此方式返回生成器，要放list()里面看具体内容
        name = list(soup.find('div',id = 'content').find('h1').stripped_strings)
        name = ''.join(name)
        #print(name)
        #获取导演名
        director = list(soup.find('div',id = 'info').find('span').find('span',class_="attrs").stripped_strings)
        director = ''.join(director)
        #print(director)
        #获取编剧名
        screenwriter = list(soup.find('div',id = 'info').find_all('span')[3].find('span',class_='attrs').stripped_strings)
        screenwriter = ''.join(screenwriter)
        #print(screenwriter)
        #获取主演名单
        actor = list(soup.find('span',class_='actor').find('span',class_='attrs').stripped_strings)
        actor = ''.join(actor)
        #print(actor)
        #获取电影评分
        score = soup.find('strong',class_="ll rating_num").string #单个标签，用string即可
        #print(score)
        #details = {}
        #details['name'] = name
        #details['director'] = director
        #details['screenwriter'] = screenwriter
        #details['actor'] = actor
        #details['score'] = score
        #print(details)
        f.write('{},{},{},{},{}\n'.format(name,director,screenwriter,actor,score))



#主函数，即入口函数
def main():
    #更改basic_url来爬取多页，观察得到规律25递增
    basic_url = 'https://movie.douban.com/top250?start={}&filter='
    # 数据保存,注意保存数据需要是字符串类型，列表不行
    with open('Top250.csv', 'a', encoding='utf-8') as f:
    #爬取多页页面u的内容，利用for循环和.format()的25递增规律
        for x in range(0,251,25):
            url = basic_url.format(x)
            detail_urls = get_detail_urls(url)
    #解析详情页面的内容，并保存数据
            parse_detail_url(detail_urls,f)

#判断语句
if __name__ == '__main__':
    main()

