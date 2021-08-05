from urllib import parse
import tkinter.messagebox as msgbox
import tkinter as tk
import re
import webbrowser
#from selenium import webdriver
#import pyttsx3 #语音模块
#from PIL import Image,ImageTk
"""原理,利用quote_plus加密后的视频链接传送给视频解析接口(即视频解析网址)"""

class APP:
    def __init__(self,width=400,height = 400):
        self.w = width
        self.h = height
        self.title = 'carson视频地址解析器'
        #在tk中指定一个classname是属性和下面的指定窗口titlr是等效的
        self.root = tk.Tk(className=self.title)
        #self.root.title (self.title)

        #创建输入框中的值的字符串对象,达到跟踪变量值变化的目的
        self.url = tk.StringVar()
        #定义 选择哪个播放器,存储数字的对象，达到跟踪变量值变化的目的
        self.v = tk.IntVar()
        #默认为1
        self.v.set(1)
        #创建两个在root之下的Frame框架
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)

        #Menu菜单
        menu = tk.Menu(self.root)
        #放置菜单栏到主窗口
        self.root.config(menu=menu)
        #控件内容设置
        group = tk.Label(frame_1,text = '5个视频解析源:',padx=10,pady=10)
        #单选框
        tb1 = tk.Radiobutton(frame_1,text='通道一',variable=self.v,value=1,width=10,height=3)
        tb2 = tk.Radiobutton(frame_1,text='通道二',variable=self.v,value=2,width=10,height=3)
        tb3 = tk.Radiobutton(frame_1,text='通道三',variable=self.v,value=3,width=10,height=3)
        tb4 = tk.Radiobutton(frame_1,text='通道四',variable=self.v,value=4,width=10,height=3)
        tb5 = tk.Radiobutton(frame_1,text='通道五',variable=self.v,value=5,width=10,height=3)
        #前面两个都是放在frame_1中,后面几个控件是放在frame_2中
        label = tk.Label(frame_2,text='请输入视频链接: ')
        #highlightthickness:控制焦点所在的高亮边框的宽度，默认值通常是1或者2像素
        entry = tk.Entry(frame_2,textvariable=self.url,highlightcolor='Fuchsia',highlightthickness=1,width=35)
        play = tk.Button(frame_2,text='播放',font=('楷体',12),fg='Purple',width=2,height=1,command=self.video_play)
        #控件布局pack()控件展示
        frame_1.pack()
        frame_2.pack()
        #grid布局方法,row行column列
        group.grid(row=0,column=0)
        tb1.grid(row=0,column=1)
        tb2.grid(row=0,column=2)
        tb3.grid(row=0,column=3)
        tb4.grid(row=0,column=4)
        tb5.grid(row=0,column=5)
        label.grid(row=0,column=0)
        entry.grid(row=0,column=1)
        #ipadx，x方向的外部填充,y方向的内部填充
        play.grid(row=0,column=3,ipadx=10,ipady=10)
        #增加视频网址的打开的按钮
        youku = tk.Button(frame_2,text='优酷视频',font=('楷体',12),fg='Purple',width=7,height=2,command=self.open_youku)
        youku.grid(row=1,column=0)
        tengxun = tk.Button(frame_2,text='腾讯视频',font=('楷体',12),fg='Purple',width=7,height=2,command=self.open_tengxun)
        tengxun.grid(row=1,column=1)
        aiqiyi = tk.Button(frame_2,text='爱奇艺',font=('楷体',12),fg='Purple',width=7,height=2,command=self.open_aiqiyi)
        aiqiyi.grid(row=1,column=2)
    #视频播放函数
    def video_play(self):
        #视频解析网站地址
        port1 = 'http://www.czjx8.com/?url='
        port2 = 'http://jx.598110.com/?url='
        port3 = 'https://jx.618g.com/?url='
        port4 = 'http://jx.cesms.cn/vip2/?url='
        port5 = 'http://www.wmxz.wang/video.php?url='
        #利用正则表达式判断是否是合法的url链接
          #^是匹配输入字符串的起始位置,$是匹配输入字符串的结束位置
          #?匹配到0次或1次,+匹配到大于等于一次,{2}限定2个
        #\w匹配字母,数字,下划线
        #.匹配除换行符 \n 之外的任何单字符
        if re.match(r'^https?:/{2}\w.+$',self.url.get()):
            #由于之前定义了stringvar(),通过变量.get()方法获取其值
            ip=self.url.get()
            #视频链接加密,用quote函数不会编码url中的/符号,用quote_pius才会编码/符号
            ip=parse.quote_plus(ip)
            #浏览器打开加密后的网址,(利用vip链接解析网址加上编码后的视频链接网址)
              #可以使用seleniium启动Chrome，也可以使用webbrowser启动IE
            if(self.v.get()==1):
                webbrowser.open(port1+ip)
                #driver = webdriver.Chrome()
                #driver.get(port+ip)
            elif(self.v.get()==2):
                webbrowser.open(port2+ip)
                #driver = webdriver.Chrome()
                #driver.get(port+ip)
            elif(self.v.get()==3):
                webbrowser.open(port3+ip)
                #driver = webdriver.Chrome()
                #driver.get(port+ip)
            elif(self.v.get()==4):
                webbrowser.open(port4+ip)
                #driver = webdriver.Chrome()
                #driver.get(port+ip)
            else:
                webbrowser.open(port5+ip)
                
        else:
            #消息提示框，弹出窗口并显示错误的信息
            msgbox.showerror(title='错误',message='视频链接地址唔对啊!')
    #打开视频网址的函数
    def open_youku(self):
        url = 'https://www.youku.com/'
        #添加语音文本
        #engine.say('即将打开优酷视频')
        #运行,每当要运行说话,都需要下面这个代码
        #engine.runAndWait()
        webbrowser.open(url)
    def open_tengxun(self):
        url = 'https://v.qq.com/'
         #添加语音文本
        #engine.say('即将打开腾讯视频')
        #运行,每当要运行说话,都需要下面这个代码
        #engine.runAndWait()
        webbrowser.open(url)
    def open_aiqiyi(self):
        url = 'https://www.iqiyi.com/'
         #添加语音文本
        #engine.say('即将打开爱奇艺视频')
        #运行,每当要运行说话,都需要下面这个代码
        #engine.runAndWait()
        webbrowser.open(url)

    #调用函数
    def loop(self):
        #root.resizable(width=False, height=False)#禁止改变窗口大小
        #这里设置可以为True,可以改变窗口的大小
        self.root.resizable(True,True)
        self.root.mainloop()

if __name__ == '__main__':
    app = APP()#实例化APP对象
    #播放语音
    #初始化
    #engine = pyttsx3.init()
    #添加语音文本
    #engine.say('程序正在启动中,欢迎您使用1204宿舍专属的VIP视频链接解析器')
    #运行,每当要运行说话,都需要下面这个代码
    #engine.runAndWait()
    app.loop() #loop等待用户事件
    


