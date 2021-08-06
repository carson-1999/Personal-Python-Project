import tkinter
import tkinter.messagebox
import random  #利用其random.shuffle()对列表进行随机打散
import threading#引入线程模块
import itertools#cylce()生成可迭代的对象利用next()进行对象的遍历
import time

def clickStart():
    #z增加子线程,防止GUI堵塞
    t = threading.Thread(target=shuffleUsers)
    t.start() #启动线程
    btnStart['state'] = 'disabled'#线程启动,启动键变不能按的状态
    btnStop['state'] = 'normal' #线程启动,停止键变为正常按钮状态


def clickStop():
    global times#利用global达到改变全局变量的目的
    root.flag = False  # 暂停线程
    time.sleep(0.1)
    times += 1
    result = showLabel['text']
    #tkinter.messagebox.showinfo(title="抽签结果:", message='第' + str(times) + '位' + ": " + showLabel['text'])
    #增加条件判断,已经抽过了的进行提示
    print(results)
    if(result in results):
        number = results.count(result)
        tkinter.messagebox.showinfo(title="抽签结果:", message=showLabel['text']+"已经选过"+str(number)+'次了!')
    else:
        tkinter.messagebox.showinfo(title="抽签结果:", message='第' + str(times) + '位' + ": " + showLabel['text'])
    results.append(result)


    btnStart['state'] = 'normal' #线程暂停,启动按钮由不能按状态变为正常按钮状态
    btnStop['state'] = 'disabled' #线程暂停,停止按钮由正常按钮变为不能按的状态


def shuffleUsers():  # 开始洗牌线程，将洗牌这个过程作为一个独立的线程进行管理
    root.flag = True
    random.shuffle(humans)
    t = itertools.cycle(humans)
    while root.flag:
        showLabel['text'] = next(t)
        time.sleep(0.1)#延缓速度

#录入数据
human_number = int(input('请输入你需要录入的人数个数:\n'))
humans = [] #存储需要抽奖的全部人
for i in range(human_number):
    human = input('请输入第%d位学生的姓名:'%(i+1))
    humans.append(human)
print('名字录入完成')

#空列表存储每次抽签的结果
results = []

#GUI界面
root = tkinter.Tk()
root.title("抽签APP")
root.geometry("300x300")
root.resizable(False, False)#设置窗口大小不可改变

root.flag = False  # 初始线程状态为False
times = 0

#开始按钮
btnStart = tkinter.Button(root, text='Start', command=clickStart)
btnStart.place(x=30, y=10, width=80, height=20)
#停止按钮
btnStop = tkinter.Button(root, text='Stop', command=clickStop)
btnStop['state'] = 'disabled' #初始化停止按钮的状态
btnStop.place(x=200, y=10, width=80, height=20)

showLabel = tkinter.Label(root, text='',font = ('Arial',18))
showLabel['fg'] = 'red' #文字前景色为红色
showLabel.place(x=100, y=180, width=100, height=20)

root.mainloop()