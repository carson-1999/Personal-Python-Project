import urllib.request
from bs4 import BeautifulSoup
import pymysql
import sys
import os
import threading

# 存取所有书本信息的列表,子元素是每本书的信息
infos = []
num = 0  # 统计存入书本信息的数目

# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                     password='root', database='mydb', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()

# 解析html页面的函数


def getHtml(url):
    # 如果出错的话,返回html的数据为空白
    html = ""
    try:
        resp = urllib.request.urlopen(url)
        data = resp.read()
        # 注意gb2312 bs4识别不了,GBK是gb2312等的父集
        html = data.decode("gbk")
    except Exception as err:
        print(err)
    return html


# 下载图片的函数
def download(image_url, title):
    try:
        # 截取出图片链接的图片的格式,用下标加切片，find是从前往后找,rfind是从后往前找
        middle = image_url.rfind('.')  # 返回其对应的下标

        if middle >= 0:
            format = image_url[middle:]
            # print(format)
        else:
            format = ''
        resp = urllib.request.urlopen(image_url)
        data = resp.read()
        with open('books\\images\\'+title+format, 'wb') as f:
            f.write(data)
    except Exception as err:
        print(err)


# 得到图书信息的函数
def getInfo(url):
    global infos
    try:
        html = getHtml(url)
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', class_='con shoplist')
        lis = div.find('ul').find_all('li')
        for li in lis:
            # 存取每本书的信息的列表
            info = []
            # 书的名称
            title = li.find('a')['title']
            info.append(title)
            # 书的图片的链接
            try:
                image_url = li.find('img')['data-original']
            except:
                image_url = li.find('img')['src']
            image_url = urllib.request.urljoin(
                url, image_url)  # 有必要的话需要拼接成完整的url链接
            # 引入多线程下载图片
            T = threading.Thread(target=download, args=[image_url, title])
            T.start()
            TS.append(T)
            # 书的价格（返回¥44.50格式,去掉￥符号）
            price = li.find('span', class_='search_now_price').text
            price = float(price[1:])
            info.append(price)
            # 书的作者
            author = li.find('p', class_='search_book_author').find('a').text
            info.append(author)

            # 出版社所在的a标签,存在即有出版社名,不存在a标签则不存在出版社名
            publisher = li.find('p', class_='search_book_author').find_all(
                'span')[2].find('a')
            # 没有出版社的话,默认出版社命名为未知
            if publisher:
                publisher = li.find('p', class_='search_book_author').find_all(
                    'span')[2].find('a').text
            else:
                publisher = 'Unknown'
            info.append(publisher)
            # 出版日期(返回 /2020-06-01,去掉/符号)
            pubDate = li.find('p', class_='search_book_author').find_all(
                'span')[1].text
            pubDate = pubDate[2:]
            # 没有日期的话，默认设置一个日期
            if pubDate == "":
                pubDate = '1111-11-11'
            info.append(pubDate)
            # 简单介绍
            brief = li.find('p', class_='detail').text
            info.append(brief)
            # 将存储每本书信息的info列表作为元素存入infos总的列表中
            infos.append(info)
            # print(title,price,author,publisher)
    except Exception as err:
        print(err)


# 数据保存至数据库(已系统中创建好了数据库mydb)
def database():
    # 构建影响全局变量
    global num
    # 数据表不存在的话则创建数据表
    sql = """create table if not exists books_info(title varchar(80) not null,price float not null,author varchar(20) not null,publisher varchar(20) not null,pubDate date,brief text not null);"""
    cursor.execute(sql)
    # 内容存入数据库,提交每本书的内容存入写入数据库中的表
    sq = "insert into books_info(title,price,author,publisher,pubDate,brief)values(%s,%s,%s,%s,%s,%s)"
    for info in infos:
        cursor.execute(
            sq, (info[0], info[1], info[2], info[3], info[4], info[5]))
        # 提交数据
        db.commit()
        num = num+1
        print("已存入"+str(num)+"本书的数据信息!")
    # 存取了一次之后需要清空一次infos列表,防止前面的重复存储
    infos.clear()


# 根据功能选择爬取多个页面打印数据,或者直接存入数据库
def spider(choose):
    # 搜寻的关键字
    keyWord = input("请输入需要查询的书籍名称:")
    # 爬取的页数
    x = int(input("请输入需要爬取的页数:"))
    for i in range(1, x+1):
        # 查找python相关书籍的各个链接
        print("开始爬取第"+str(i)+"页")
        url = 'http://search.dangdang.com/?key={}&act=input&page_index={}'.format(
            keyWord, i)
        # 打印目前已存在列表的书的数目
        print(len(infos))
        # 进行是否存入数据库的功能选择
        if choose == 1:
            # 爬取每一个url
            getInfo(url)
        elif choose == 2:
            # 爬取每一个url
            getInfo(url)
            # 存入数据库
            database()
        else:
            print("功能选择错误,只能输入1(代表爬取页面但不存入数据库),输入2(将数据存入数据库)")


# 查看数据库中的数据
def data():
    try:
        # 数据表不存在的话则创建数据表
        sql = """create table if not exists books_info(title varchar(80) not null,price float not null,author varchar(20) not null,publisher varchar(20) not null,pubDate date,brief text not null);"""
        cursor.execute(sql)
        sq = "select * from books_info"
        cursor.execute(sq)
        results = cursor.fetchall()
        if results:
            for result in results:
                print(result)
        else:
            print("数据表为空")
    except Exception:
        pass


# 清空数据库中的数据
def clear_database():
    try:
        sq = "delete from books_info"
        cursor.execute(sq)
        db.commit()  # 数据库涉及到数据改动需要进行提交
        results = cursor.fetchall()
        if results:
            for result in results:
                print(result)
        else:
            print("数据表已清空")
    except Exception as err:
        print(err)

# 清空文件夹


def clear_dir():
    if os.path.exists('books\\images'):
        position = os.getcwd()+'\\books'+"\\images\\"
        # print(position)
        for photo in os.listdir('books\\images'):
            os.remove(position+photo)
        print("images文件夹中的图片已清空!")
    else:
        print("images文件夹不存在")


if __name__ == "__main__":
    print("-"*30+"爬取当当网图书"+"-"*30)
    # 创建图片文件夹
    if not os.path.exists('books\\images'):
        os.mkdir('books\\images')
    # 多线程的线程列表
    TS = []
    while True:
        print("1代表爬取数据并进行是否存入数据库的选择\n2代表查看数据库中的数据\n3代表清空数据库\n4代表清空图片文件夹\n5代表退出程序")
        number = int(input("请输入功能选择数字:"))
        if number == 1:
            choose = int(
                input("输入1或者2进行功能选择！输入1(代表爬取页面但不存入数据库),输入2(将数据存入数据库))"))
            spider(choose)
            # 有线程退出就加入
            for T in TS:
                T.join()
            print('Bye!')
        elif number == 2:
            data()
        elif number == 3:
            clear_database()
        elif number == 4:
            clear_dir()
        elif number == 5:
            # 关闭数据库连接后退出
            db.close()
            print("已退出！")
            break
