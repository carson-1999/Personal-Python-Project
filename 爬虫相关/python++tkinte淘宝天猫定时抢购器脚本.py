from selenium import webdriver
import datetime
from  threading import Thread
from  tkinter import *
import tkinter as tk
import time
import pyttsx3


#初始化
engine = pyttsx3.init()
#设置音量最大
engine.setProperty('volume', 1.0)

#GUI界面
#初始化GUI界面
root = Tk()
root.title('淘宝天猫定时抢购器')
root.geometry('400x350')

"""#增加背景图片
canvas = tk.Canvas(root,height=350,width = 400)
image = Image.open('1.jpg')
photo = ImageTk.PhotoImage(image)
canvas.create_image(0,0,anchor='nw',image=photo)
canvas.pack()"""


lb1 = Label(root,text = '注意:打开手机淘宝扫码进行登陆(请30秒内完成登陆)',font=('Arial', 12))
lb1.place(relx = 0.02,rely=0.03)
lb2 = Label(root,text = '商品的链接:',font=('Arial', 11))
lb2.place(x = 20,y = 45)

entry1_str = StringVar()
entry1_str.set('请在此输入商品的链接')
entry1 = Entry(root,textvariable = entry1_str,)
entry1.place(x = 15,y = 68,height=28,width=350)

lb3 = Label(root,text = '选择购买的商品所属的商城:',font=('Arial', 11))
lb3.place(x = 20,y = 102)

#单选框
v = IntVar()
#默认为1
v.set(1)
tb = tk.Radiobutton(root,text='淘宝商城',variable=v,value=1,width=10,height=1,font=('Arial', 10))
tm = tk.Radiobutton(root,text='天猫商城',variable=v,value=2,width=10,height=1,font=('Arial', 10))
tb.place(x = 40,y=128)
tm.place(x = 200,y=128)


lb4 = Label(root,text = '输入开售时间【格式如:2021-01-15 12:55:50】',font=('Arial', 11))
lb4.place(x = 20,y = 161)

entry2_str = StringVar()
entry2_str.set('请在此输入抢购时间,格式如:2021-02-01 12:55:50')
entry2 = Entry(root,textvariable = entry2_str,)
entry2.place(x = 15,y = 185,height=29,width=360)

lb5 = Label(root,text = '注意:',font=('Arial', 11))
lb5.place(x = 10,y = 215)
lb6 = Label(root,text = '进入商品页面需提前选好商品规格,然后等待时间到即可自动购买',font=('Arial', 10))
lb6.place(x = 6,y = 235)




#扫码登陆函数
def login(url,mall,driver):
    '''
    登陆函数
    url:商品的链接
    mall：商城类别
    '''
    driver.get(url)
    driver.implicitly_wait(10)
    #淘宝和天猫的登陆链接文字不同
    if mall==1:
        close = 'body > div.baxia-dialog.auto > div.baxia-dialog-content > div'
        driver.find_element_by_css_selector(close).click()
        time.sleep(2)
        #找到并点击淘宝的登陆按钮
        driver.find_element_by_link_text("亲，请登录").click()
        #点击二维码登陆
        time.sleep(0.5)
        erweima = '#login > div.corner-icon-view.view-type-qrcode > i'
        driver.find_element_by_css_selector(erweima).click()
    else:
        close = 'body > div.baxia-dialog.auto > div.baxia-dialog-content > div'
        driver.find_element_by_css_selector(close).click()
        time.sleep(1.5)
        #找到并点击天猫的登陆按钮
        driver.find_element_by_link_text("请登录").click()
        #点击二维码
        #time.sleep(2)
        #erweima = '#login > div.corner-icon-view.view-type-qrcode > i'
        #driver.find_element_by_css_selector(erweima).click()
    engine.say('请在30秒内完成扫码登录')
    #运行,每当要运行说话,都需要下面这个代码
    engine.runAndWait()
    print("请在30秒内完成登录")
    #用户扫码登陆
    time.sleep(30)

#购买商品函数
def buy(buy_time,mall,driver):
    '''
    购买函数
    
    buy_time:购买时间
    mall:商城类别
    
    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    css_selector的方式表现最佳
    '''
    if mall== 1:
        #"立即购买"的css_selector
        btn_buy='#J_juValid > div.tb-btn-buy > a'
        #"立即下单"的css_selector
        btn_order='#submitOrderPC_1 > div.wrapper > a'
       
    else:
        btn_buy='#J_LinkBuy'
        btn_order='#submitOrderPC_1 > div > a'
        
        
    while True:
        #现在时间大于预设时间则开售抢购
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')>=buy_time:
            try:
                #找到“立即购买”，点击
                if driver.find_element_by_css_selector(btn_buy):
                    driver.find_element_by_css_selector(btn_buy).click()
                    break
                time.sleep(0.1)
            except:
                time.sleep(0.3)
    
    while True:
        try:
            #找到“立即下单”，点击，
            if driver.find_element_by_css_selector(btn_order):
                driver.find_element_by_css_selector(btn_order).click()
                #下单成功，跳转至支付页面
                print("购买成功")
                engine.say('购买成功 ')
                #运行,每当要运行说话,都需要下面这个代码
                engine.runAndWait()
                break
        except:
            time.sleep(0.5)

def main():
    #创建浏览器窗口
    # 创建浏览器对象
    driver = webdriver.Chrome()
    # 窗口最大化显示
    driver.maximize_window()
    #获取信息
    #Thread(target=lambda: login(entry1_str.get(), v.get(), driver)).start()
    url = entry1_str.get()
    mall = v.get() #由于输入的数字是整形
    #print(mall,type(mall))
    buy_time = entry2_str.get()
    login(url,mall,driver)
    buy(buy_time,mall,driver)

#引入多线程防止在点击按钮的时候卡死
#Thread(target=lambda: login(entry1_str.get(), v.get(),driver)).start()
def run():
    t = Thread(target=main)
    t.start() #启动线程

if __name__ == "__main__":
    # 购买按钮
    bt2 = Button(root, text='立即抢购', font=('Arial', 14), command=run)
    bt2.place(x=130, y=295)
    root.mainloop()  # 加载GUI界面输入信息后再执行购票程序

