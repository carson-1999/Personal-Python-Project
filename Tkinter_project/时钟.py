from tkinter import  *
import time

def gettime():
    time_current = time.strftime("%H:%M:%S")# 获取当前时间并转换为字符串
    lb.configure(text = time_current)     # 重新设置标签文本
    root.after(1000,gettime)      # 每隔1S调用函数 gettime 自身获取时间

root = Tk()
root.title('时钟')

lb = Label(root,text = '',fg = 'green',font = ('黑体',80))
lb.pack()
gettime()
root.mainloop()