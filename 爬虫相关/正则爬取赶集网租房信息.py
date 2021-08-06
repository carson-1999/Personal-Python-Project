#爬取一页为例，爬取多页的话根据url递增规则即可
import  re
import  requests

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

"""解析详情页内容并保存文件"""
def parse_page(url,f):
    resp = requests.get(url,headers = headers)
    text = resp.text
    #不同于xpath和bs4的树状查找，用正则数据解析，利用分组获取特定信息
    #目标标题在div标签下的特定class的a标签下的文本内容中
    #注意.不适用\n换行符，需要后面加上表示用|连接re.DOTALL
    houses = re.findall(r"""
    <div.+?ershoufang-list".+?<a.+?js-title.+?>(.+?)</a>  #获取房源的标题
    .+?<dd.+?dd-item.+?<span>(.+?)</span>  #获取房源的户型
    .+?<span.+?<span>(.+?)</span>    #获取房源面积
    .+?<span.+?<span>(.+?)</span>    #获取房源朝向
    .+?<span.+?<span.+?">(.+?)</span>    #获取房源装修情况
    .+?<div.+?price.+?<span.+?num">(.+?)</span>  #获取房源价格
    """,text,re.VERBOSE|re.DOTALL)
    for house in houses:
        #print(house)
        f.write('{},{},{},{},{},{}\n'.format(house[0],house[1],house[2],house[3],house[4],house[5]))



def main():
    basic_url = 'http://shantou.ganji.com/zufang/pn{}/'
    #爬取多页，爬个10页
    with open('houses.csv','a',encoding='utf-8') as f:
        f.write('{},{},{},{},{},{}\n'.format('标题','户型','面积','朝向','装修情况','月租'))
        for x in range(1,11):
            url = basic_url.format(x)
            parse_page(url,f)


if __name__ == '__main__':
    main()
