import  requests
from lxml import  etree

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36','Cookie': 'uuid=dabb5d13-2113-4848-f08c-3cdb5b3eb037; user_city_id=19; ganji_uuid=1396219145883636473885; lg=1; antipas=17G701618ySk6762r67048g04; clueSourceCode=%2A%2300; sessionid=0a1083bd-97d5-41a6-806b-1562c9b5c596; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1594894513,1594964155; close_finance_popup=2020-07-17; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A49084183770%7D; cityDomain=shantou; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22dabb5d13-2113-4848-f08c-3cdb5b3eb037%22%2C%22ca_city%22%3A%22shantou%22%2C%22sessionid%22%3A%220a1083bd-97d5-41a6-806b-1562c9b5c596%22%7D; preTime=%7B%22last%22%3A1594965300%2C%22this%22%3A1594894509%2C%22pre%22%3A1594894509%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1594965302'
}


#//ul[@class="carlist clearfix js-top"]
"""函数封装，获取各个详情页面的URL"""
def get_detail_urls(url):
    # 获取其网页源代码
    resp = requests.get(url, headers=headers)
    # 将其储存在变量当中
    text = resp.content.decode('utf-8')
    print(text)
    # html处理
    html = etree.HTML(text)
    # xpath语法处理提取,下标0是取5个列表元素的第一个元素
    ul = html.xpath('//ul[@class="carlist clearfix js-top"]')[0]
    list = ul.xpath('./li')
    detail_urls = []  # 添加空列表
    for li in list:
        detail_url = li.xpath('./a/@href')
        detail_url = 'https://www.guazi.com' + detail_url[0]
        # print(detail_url)
        detail_urls.append(detail_url)  # 添加到空列表
    return detail_urls  # 注意缩进，要在循环外，返回所有的urls列表


"""函数封装,获取隐藏的上牌时间图片的链接"""
def get_photo_links(detail_urls):
    # 创建空列表
    photo_links = []
    for detail_url in detail_urls:
        resp = requests.get(detail_url, headers=headers)
        text = resp.content.decode('utf-8')
        # 解析HTML代码
        html = etree.HTML(text)
        # xpath数据提取,获取根节点,加下标0是获取列表的具体内容
        photo_link = html.xpath('//div[@class = "product-textbox"]')[0]
        # 返回的是列表，加下标0是获取列表的具体内容
        photo_link = photo_link.xpath('./ul/li/span/img/@src')[0]
        photo_links.append(photo_link)
    return photo_links


"""函数封装，获取详情页右边三个信息"""
def parse_detail_page(detail_urls):
    # 遍历每个detail_url进行数据解析
    for detail_url in detail_urls:
        resp = requests.get(detail_url, headers=headers)
        text = resp.content.decode('utf-8')
        # 解析HTML代码
        html = etree.HTML(text)
        # xpath数据提取，获取标题信息
        title = html.xpath('//div[@class = "product-textbox"]/h2/text()')[0]
        title = title.replace(r'\r\n', '').strip()
        # print(title)
        infos = {}  # 创建空字典
        """获取下面四个标签信息"""
        # 由于日期时间采用了图片的形式，所以下面打印三个信息,三个对应5个元素的下标234
        infomation = html.xpath('//div[@class = "product-textbox"]/ul/li/span/text()')
        # 列表元素提取
        KM = infomation[2]
        displacement = infomation[3]
        speedbox = infomation[4]
        # xpath数据提取,获取根节点,加下标0是获取列表的具体内容
        photo_link = html.xpath('//div[@class = "product-textbox"]')[0]
        # 返回的是列表，加下标0是获取列表的具体内容
        photo_link = photo_link.xpath('./ul/li/span/img/@src')[0]
        #添加到空字典信息
        infos['title'] = title
        infos['KM'] = KM
        infos['displacement'] = displacement
        infos['speedbox'] = speedbox
        infos['photo_link'] = photo_link
        #打印字典
        #print(infos)
        return infos

"""数据保存"""
def save_data(infos,f):
    f.write('{},{},{},{},{}\n'.format(infos['title'],infos['KM'],infos['displacement'],infos['speedbox'],infos['photo_link']))

def main():
    #第一个访问的url
    url = 'http://www.guazi.com/cs/buy/o1/'
    #for x in range(1,4):
        #url = basic_url.format(x)
    with open('guazi.csv','a',encoding='utf-8') as f:
            #函数调用，获取详情页url
        detail_urls = get_detail_urls(url)
            #调用函数，获取详情页的内容
        for detail_url in detail_urls:
            infos = parse_detail_page(detail_url)
            save_data(infos,f)

if __name__ == '__main__':
    main()

























