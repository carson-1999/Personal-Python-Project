from tkinter import * #编写GUI界面
import tkinter as tk
import threading  #引入线程,解决GUI堵塞
from selenium import webdriver
#导入显式等待相关库
from selenium.webdriver.support.ui import WebDriverWait
#导入显式等待条件语句库
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By #后面的until()必须元组形式，所以导入By
#导入csv模块来读取站点代号
import  csv
#导入表单下滑选项操作的库
from selenium.webdriver.support.ui import Select
#导入可能出现的异常
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
#导入时间模块进行等待
from time import sleep
#导入发送邮件模块
import yagmail
from PIL import ImageTk,Image
import requests


"""将driver放在外面的原因是：
   如果放在里面，那么driver将会随着对象的销毁而销毁
   而我们的类TrainSpider的实例对象是放在main()函数中执行的
   只要main()函数运行完成后，里面所有的变量都会被销毁
   也就说spider类实例对象也会被销毁
"""

#初始化GUI界面
root = Tk()
root.title('Carson的12306购票器')
root.geometry('400x350')

#增加背景图片
'''canvas = tk.Canvas(root,height=350,width = 400)
image = Image.open('1.jpg')
photo = ImageTk.PhotoImage(image)
canvas.create_image(0,0,anchor='nw',image=photo)
canvas.pack()'''

#初始化基本GUI界面的组件
lb1 = Label(root,text = '欢迎使用Carson的12306二等座购票器',font=('Arial', 14))
lb1.place(relx = 0.08,rely=0.02)
lb2 = Label(root,text = '乘车人员:',font=('Arial', 12))
lb2.place(x = 45,y = 45)
lb3 = Label(root,text = '出发日期:',font=('Arial', 12))
lb3.place(x = 45,y = 78)
lb4 = Label(root,text = '出发车站:',font=('Arial', 12))
lb4.place(x = 45,y = 111)
lb5 = Label(root,text = '终点车站:',font=('Arial', 12))
lb5.place(x = 45,y = 144)
lb6 = Label(root,text = '购买车次:',font=('Arial', 12))
lb6.place(x = 45,y = 177)
lb7 = Label(root,text = '购票信息如下:',font=('Arial', 12))
lb7.place(x = 0,y = 205)
text = Text(root,height = 5,width=56)
text.place(x = 0,y= 232)
#text.insert('0.0','需要字典形式，形式如：{“G529”:["O"]}多车次就多个键值对')
#text.insert('0.0','默认已选的车次:{"D7432":["O"],"G6316":["O"],"D2336":["O"],"D2328":["O"],"G1610":["O"],"D7448":["O"],"D3338":["O"],"D672":["O"],"G6312":["O"],"D3334":["O"],"D3340":["O"],"D3342":["O"],"G6082":["O"],"D7428":["O"],"D690":["O"],"D2332":["O"],"D7312":["O"],"G6006":["O"]}')
entry1_str = StringVar()
entry1_str.set('输入乘车人的姓名,如:张三')
entry1 = Entry(root,textvariable = entry1_str,)
entry1.place(x = 120,y = 46,height=28,width=160)
entry2_str = StringVar()
entry2_str.set('输入出发日期,格式如:2021-01-16')
entry2 = Entry(root,textvariable = entry2_str,)
entry2.place(x = 120,y = 79,height=28,width=190)
entry3_str = StringVar()
entry3_str.set('输入起始站,如:深圳北')
entry3 = Entry(root,textvariable = entry3_str)
entry3.place(x = 120,y = 112,height=28,width=160)
entry4_str = StringVar()
entry4_str.set('输入终点站,如:潮阳')
entry4 = Entry(root,textvariable = entry4_str)
entry4.place(x = 120,y = 145,height=28,width=160)
entry5_str = StringVar()
entry5_str.set('输入车次,格式如:D2325 G6347')
entry5 = Entry(root,textvariable = entry5_str)
entry5.place(x = 120,y = 178,height=28,width=180)
class TrainSpider:  
    #将属性放类里面定义为类属性
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html' #二维码登陆界面url
    personal_url = 'https://kyfw.12306.cn/otn/view/index.html'  #登陆后进入的个人中心url
    left_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc' #查询车次和余票的url
    confirm_passenger_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc' #确认乘客信息的url
    
    def __init__(self,from_station,to_station,train_date,trains,passengers,driver):
        """
        :param from_station:  起始车站
        :param to_station: 目的地车站
        :param train_date: 出发日期
        :param trains: 需要购买的车次。需要字典形式，形式如：{“G529”:["O","M"],"G403":["O","M"]}多车次就多个键值对
        :param passengers: 需要买票的乘车人，需要为一个列表
        """
        self.driver = driver
        self.from_station = from_station
        self.to_station = to_station
        self.train_date = train_date
        self.trains = trains
        self.passengers = passengers
        self.current_number = None #定义一下变量保存下当前预定的车次序号信息
        self.current_seat = None #定义一下变量保存下当前选中的车次的选中的席位信息
        #为了方便根据站名文字来取得车站代号，需要创建字典存储代号数据
        #且空集合的创建要在函数外，不然执行完函数集合数据就没有了
        self.station_codes = {}
        #初始化站点代号数据
        self.get_station_codes()


    #获取车站代码
    def get_station_codes(self):
        #读取数据并存放到空字典中
        with open('stations.csv', 'r', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            for line in reader:
                name = line['name']
                code = line['code']
                self.station_codes[name] = code


    #实现登陆功能
    def login(self):
        self.driver.maximize_window() #最大化窗口
        # 将属性放类里面定义为类属性,调用时需要加self进行调用
        self.driver.get(self.login_url)
        # 进行显式等待(有条件)设置100秒，且用来判断是否登陆成功
        # 即后面判断条件是url是否变化成个人中心的url
        WebDriverWait(self.driver, 100).until(
            EC.url_to_be(self.personal_url)  # 注意类中变量调用加self
            #或者EC.url_contains(self.personal_url)
        )
        print('登陆成功!')
        print('开始刷票！')


    #查询车次余票
    def search_left_tickets(self):
        self.driver.get(self.left_ticket_url)
        """起始站的代号设置"""
        from_station_input = self.driver.find_element_by_id('fromStation')
        #利用用户输入文字获取起始站的代号
        from_station_code = self.station_codes[self.from_station]
        #通过js代码修改隐藏标签的value值来达到输入起始站的目的
        self.driver.execute_script("arguments[0].value = '%s'"%from_station_code,from_station_input)
        """终点站的代号设置"""
        to_station_input = self.driver.find_element_by_id('toStation')
        to_station_code = self.station_codes[self.to_station]
        self.driver.execute_script("arguments[0].value = '%s'"%to_station_code,to_station_input)
        """日期设置"""
        #这里没有前面两个复杂，没有被隐含，理论上标签send_keys即可
        #但可能也像前面两个输入框一样被处理过，故输入时间也才用执行js代码的方式
        train_date_input = self.driver.find_element_by_xpath('//*[@id="train_date"]') #xpath*表任意
        self.driver.execute_script("arguments[0].value = '%s'" % self.train_date, train_date_input)
        """执行查询操作"""
        search_button = self.driver.find_element_by_id('query_ticket').click()
        print("第1次查询中...")
        # 因为点击查询按钮后需等待一下才会返回列车车次数据
        # 所以在解析具体的车次信息前需要设置等待,采用显示等待(条件即加载出tbody下的tr标签)
        """注意,在until(EC.presence_of_element_located())中
        验证元素是否出现，传入的参数必须都是元组类型的locator，如(By.ID, ‘kw’)，
        不能传入webelement对象，即driver.find_elemet_by_id()的写法不行会报错
        """
        # 设置1000秒显式等待有各个列车信息的tr标签出现(一般开售前5分种即5*60=300秒足够了）
        WebDriverWait(self.driver, 1000).until(
            # 条件判断是某元素即tr标签是否出现，注意..located()里面是元组类型的locator，必须如下写法
            EC.presence_of_element_located((By.XPATH, '//*[@id="queryLeftTable"]/tr'))
        )
        # 注意有许多车次对应许多的tr标签，注意用elements返回列表
        # 且注意对第二个tr标签利用xpath里面的not(@属性名)过滤掉
        trains = self.driver.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr[not(@datatran)]')
        #添加一个布尔标志，用于判断所选车次是否有票再去查询
        is_searched = False
        n =1
        #添加死循环，直到数据符合条件才退出
        while True:
            for train in trains:
                # 利用text打印出标签里面关于车次信息的文本即可
                # 由于刚打印出来的数据之间都是换行的，现在将其替换空格放成同一行
                # 调用split()，以空格进行分割，分割上面替换后的字符串,会返回列表形式的车次的所有信息
                infos = train.text.replace("\n", ' ').split(' ')
                # 从返回的车次列表信息中提取出车次序号数据
                number = infos[0]
                # 判断提取的车次序号数据(number)有没有在用户要的车次字典的里面
                # 是的话再判断有无席位的信息再去预定,
                if number in self.trains:  # 注意self.trains我们已定义是字典，{“G529":["O"."M"]}
                    seat_types = self.trains[number]  # 根据numer的键取得定义字典的座席类型
                    # 取得的座位类型是列表，需要for循环遍历
                    for seat_type in seat_types:
                        # 当座位席位是二等座时，且二等座对应infos[9]
                        if seat_type == "O":
                            count = infos[9]
                            # 当count是数字或者是有 时代表有座
                            # 用.isdigtit()方法说明是数字
                            if count.isdigit() or count == '有':
                                is_searched = True
                                break  # 找到一个座位类型就可以退出自己想要的座位类型列表了
                        # 当座位席位是一等座时，且一等座对应infos[8]
                        elif seat_type == "M":
                            count = infos[8]
                            if count.isdigit() or count == '有':
                                is_searched = True
                                break  # 找到一个座位类型就可以退出自己想要的座位类型列表了
                # 当有票即布尔标志为True时执行预定按钮
                if is_searched:
                    self.current_number = number  # 保存下当前选择的车次序号信息
                    # 从train即第一个有数据的tr标签里面用xpath去找预定按钮执行预定
                    order_button = train.find_element_by_xpath('.//a[@class="btn72"]')
                    order_button.click()
                    print(str(number)+"车次有票,当前购买的车次是"+str(number))
                    # 当有票且执行预定了的话，买到票了，就可以退出最外层的对车次解析的循环了
                    return#不能用break只能退出for，return才能退出死循环

            # 当标志为False时,不断执行查询操作
            if is_searched==False:
                try:
                    search_button = self.driver.find_element_by_id('query_ticket')
                    search_button.click()
                    n += 1
                    #trains也要在每次查询点击后再重新查找一下,即更新trains元素
                    trains = self.driver.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr[not(@datatran)]')
                    print("第%d次查询中..."%n)
                    #设置等待，让其监控余票
                    sleep(4)

                except StaleElementReferenceException: #俘获异常则pass
                    pass


    def confirm_passengers(self):
        #需要显示等待下，确认下url是否已经变化到确认乘客信息
        WebDriverWait(self.driver,100).until(
            #EC.url_to_be(self.confirm_passenger_url)
            EC.url_contains(self.confirm_passenger_url)
        )
        #需要再显示等待下，确认下乘车人的横栏信息是否加载出来了
        WebDriverWait(self.driver,100).until(
            EC.presence_of_element_located((By.XPATH,'//ul[@id="normal_passenger_id"]/li/label'))
        )
        """确认需要购买的乘客"""
        #需要找到多个li标签下的label，需要elements且返回列表
        passenger_lables = self.driver.find_elements_by_xpath('//ul[@id="normal_passenger_id"]/li/label')
        for passenger_lable in passenger_lables:
            name = passenger_lable.text
            #判断这个获取的name在不在所要买票的人的列表里
            if name in self.passengers:  #注意是列表形式的数据才能用in
                passenger_lable.click() #勾选起来即可

        """确认需要购买的座位类型"""
        #先用Select()包装下
        seat_select = Select(self.driver.find_element_by_id('seatType_1'))
        #下面选择席位，需要根据用户能够接受的席位来选择
        #这步的话有个细节，前面需要保存下之前预定按钮选择的车次序号，以便根据序号来看看对应用户需要的座位类型
        seat_types = self.trains[self.current_number]  # 使用相应的key值查找对应车次序号的座位类型列表
        for seat_type in seat_types:
            #注意细节，假如第一个选择的席位没有票了，选择不到，会抛出异常
            try:
                self.current_seat = seat_type #保存一下当前选泽的席位信息
                seat_select.select_by_value(seat_type)
            except NoSuchElementException:
                continue
            else:
                break  #假如第一个有票就直接选择然后退出循环

        #等待提交按钮可以被点击
        WebDriverWait(self.driver,100).until(
            #即等待某个元素可以被点击
            EC.element_to_be_clickable((By.ID,'submitOrder_id'))
        )
        sumit_button = self.driver.find_element_by_id('submitOrder_id')
        sumit_button.click()

        #判断模态对话框即购票信息对话框出现并确认按钮可以点击了
        WebDriverWait(self.driver,100).until(
            EC.presence_of_element_located((By.CLASS_NAME,'dhtmlx_window_active'))
        )
        WebDriverWait(self.driver,100).until(
            EC.element_to_be_clickable((By.ID,'qr_submit_id'))
        )
        sumit_button = self.driver.find_element_by_id('qr_submit_id')
        #注意这里的细节，由于Seenium自身的Bug，可能会导致确认点击操作无法正确执行
        #故需俘获异常，且需加入无限循环操作，点击之后再获取再点击
        try:
            while sumit_button:
                try:
                    sumit_button.click()
                    sumit_button = self.driver.find_element_by_id('qr_submit_id')
                except (ElementNotVisibleException,ElementNotInteractableException): #当在此页面见不到此元素，代表已进入付款页面
                    break
            print("恭喜鲁！%s车次%s席位抢票成功"%(self.current_number,self.current_seat))
        except:
            pass

    def send_mail(self):
        #推送消息到微信server酱
        #同样内容的消息一分钟只能发送一次，服务器只保留一周的消息记录。

        url = 'https://sc.ftqq.com/SCU136031Td1bc5351012e91530cbd1f55472c55dc5fd97efb248ee.send'
        title = "恭喜鲁！%s的%s车次二等座购票成功"%(self.passengers,self.current_number)
        data = {'text':title,'desp':'Nice,666!'}
        r =requests.post(url,data)
        #信息量化,并体现为字符串中含有 某字符串 作为 条件判断
        if "success" in r.text:
            print("购票成功,已经推送到微信")
        """发送邮件"""
        # 连接服务器，提供用户名,授权码,服务器地址
        yag_server = yagmail.SMTP(user='1105853259@qq.com', password='zkglfobahmzwjjjh', host='smtp.qq.com')
        # 填写发送对象，邮件主题和内容
        email_to = ['2429070946@qq.com', ]
        email_title = "恭喜鲁！%s的%s车次二等座购票成功"%(self.passengers,self.current_number)
        #由于self.passengers是列表的形式,要转为str进行拼接然后加[0]提取内容
        email_content = "乘车人:"+str(self.passengers[0])+"\n"+"出发日期:"+str(self.train_date)+"\n"+"所买车次:"+str(self.current_number)+"\n"+"所买路线:"+str(self.from_station)+"------>>"+str(self.to_station)
          
        # 发送邮件
        yag_server.send(email_to, email_title, email_content)
        print('购票成功,已发送邮件！')
        # 关闭服务
        yag_server.close()


    """写个run方法,将步骤封装在一起,让使用起来更方便，即不用理里面的细节"""
    def run(self):
        #先登陆
        self.login()
        #查车次余票
        self.search_left_tickets()
        #确认乘客和车次信息
        self.confirm_passengers()
        #购票后发送邮件通知
        self.send_mail()

#引入线程,target是main函数,防止GUI堵塞
def run():
    t = threading.Thread(target=main)
    t.start() #启动线程
    
#输出信息函数
def printlog():
    #提取输入的数据
    name = entry1_str.get()
    date = entry2_str.get() 
    start_station = entry3_str.get()
    stop_station = entry4_str.get()
    train_s = entry5_str.get()
    #打印个人信息
    info='乘车人:'+name+"\n"+"出发日期:"+date+"\n"+"路线:"+start_station+"---->>"+stop_station+"\n"+"所选车次:"+train_s
    text.insert(END,info)

#运行函数
def main():
    #由12306座位类型的代号设置如下
    #9：商务座 M：一等座 O：二等座 3：硬卧 4：软卧 1：硬座      注意:G6006车次7点27出发，9点16到是【复兴号】
    #spider = TrainSpider('深圳北','潮阳','2021-01-17',{"D7432":["O"],"G6316":["O"],"D2336":["O"],"D2328":["O"],"G1610":["O"],"D7448":["O"],"D3338":["O"],"D672":["O"],"G6312":["O"],"D3334":["O"],"D3340":["O"],"D3342":["O"],"G6082":["O"],"D7428":["O"],"D690":["O"],"D2332":["O"],"D7312":["O"],"G6006":["O"]},['张盛滨',])
    #spider = TrainSpider(start_station,stop_station,date,{"D7432":["O"],"G6316":["O"],"D2336":["O"],"D2328":["O"],"G1610":["O"],"D7448":["O"],"D3338":["O"],"D672":["O"],"G6312":["O"],"D3334":["O"],"D3340":["O"],"D3342":["O"],"G6082":["O"],"D7428":["O"],"D690":["O"],"D2332":["O"],"D7312":["O"],"G6006":["O"]},[name,])
    #初始化chromedriver
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    name = entry1_str.get()
    date = entry2_str.get() 
    start_station = entry3_str.get()
    stop_station = entry4_str.get()
    train_s = entry5_str.get()
    train_infos = train_s.split(' ')#以空格符为分界形成车次信息列表
    trains = {} #创建空字典存储车次信息
    for train_info in train_infos:
        trains[train_info] = ["O"]  #默认都选为O二等座,然后加入空字典
    spider = TrainSpider(start_station,stop_station,date,trains,[name,],driver)
    spider.run()

#输出所填的信息确认
bt2 = Button(root,text = '输出购票信息',font=('Arial', 14),command=printlog)
bt2.place(x= 20,y= 307)
#按钮事件执行时间过长,引入线程,
bt2 = Button(root,text = '确认无误,开始刷票',font=('Arial', 14),command=run)
bt2.place(x= 200,y= 307)

root.mainloop() #加载GUI界面输入信息后再执行购票程序

#if __name__ == '__main__':
    #main()
