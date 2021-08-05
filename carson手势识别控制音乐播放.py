from aip import AipBodyAnalysis#导入百度aip包
import pyautogui#模拟键盘按键依赖库
import cv2 as cv #读取显示摄像头
from threading import Thread #引入线程，防堵塞
from time import sleep #一个操作完成后进行停歇处理
import pyttsx3  #语音模块
import os #删除文件
from time import sleep
import requests #捕获其请求异常
import sys #关闭程序

"""pyautogui.hotkey('win', 'r')
sleep(1)
pyautogui.hotkey('delete')
pyautogui.click(114,892)
pyautogui.typewrite('regedit')
pyautogui.hotkey('enter')
#获取光标的位置
X,Y = pyautogui.position()"""

#初始化
engine = pyttsx3.init()
#设置音量最大
engine.setProperty('volume', 1.0)

#定义变量，申请百度AI账号的的三个ID
AppID = '######'
APIKey = '######'
SecretKey = '#######'

client = AipBodyAnalysis(AppID,APIKey,SecretKey)

#读取摄像头
capture = cv.VideoCapture(0)
def camera():
    while True:
        ret,frame = capture.read()
        if ret:
            cv.imshow('Music_Control',frame)
        if cv.waitKey(1) == 27:#返回键
            break
        
#引入多线程防止在识别的时候卡死
Thread(target=camera).start()

#读取图的函数
"""def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()"""
    
#调用函数读取图像
#image = get_file_content('2.png')

#创建识别结果的对应字典
hand = {'Prayer':'祈祷','Palm_up':'掌心向上','Heart_3':"双手比心",'Ok':'OK','One':'数字1','Two':'数字2','Five':'数字5','Fist':'拳头','Heart_single':'比心','Thumb_up':'点赞','Thumb_down':'Diss','Rock':'摇滚'}

#自动关闭三个代理按钮的函数
def close():
    pyautogui.click(25,1055)
    sleep(0.5)
    pyautogui.click(20,944)
    sleep(0.5)
    pyautogui.click(739,483)
    sleep(0.5)
    pyautogui.click(571,755)
    sleep(0.5)
    pyautogui.click(965,344)
    sleep(0.5)
    pyautogui.click(958,428)
    sleep(0.5)
    pyautogui.click(960,796)
    sleep(0.5)
    pyautogui.click(1758,71)
    print("代理按钮已关闭")

#控制音量加大
def higher():
    pyautogui.click(1654,1051)
    sleep(0.5)
    pygutogui.press('up')
    #pyautogui.keyDown('right')
    #pyautogui.keyUp('right')


#控制音量减小
def lower():
    pyautogui.click(1654,1051)
    sleep(0.5)
    pygutogui.press('down')
    #pyautogui.keyDown('left')
    #pyautogui.keyUp('left')
    


#清除自动代理的脚本
def clear():
    path = 'C:\\Users\\张盛滨\\AppData\\Local\\Microsoft\\Internet Explorer\\MS_PUB_ACCOUT'
    if os.path.exists(path):
        print("文件存在，即将删除")
        os.remove(path)
        print('文件已删除')
        close()
        print("代理按钮已关闭")
    else:
        print("代理文件不存在")

#将摄像头截取的每一帧图片传入识别手势
def gesture_recognition():
    while True:
        try:
            ret,frame = capture.read()
            if ret:
                cv.imshow('Music_Control', frame)
                #图片格式转换
                image = cv.imencode('.jpg',frame)[1]# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
                #print(image)
                #AipBodyAnalysis内部函数
                gesture = client.gesture(image)
                print(gesture)
                words = gesture['result'][0]['classname']
                result = hand[words]
                #voice(hand[words])#调用字典对应值读出来
                print("手势识别结果是:",result)
                #切换下一曲
                if result == '点赞':
                    #添加语音文本
                    #engine.say('即将切换到下一首歌!')
                    engine.say('OK!About to switch to the next song')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    pyautogui.hotkey('ctrl', 'alt', 'right')
                    print('已切换到下一首歌!')
                    sleep(2)
                #切换到上一曲
                elif result == '数字2':
                    #添加语音文本
                    #engine.say('即将切换到上一首歌!')
                    engine.say('OK!About to switch to the previous song')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    
                    pyautogui.hotkey('ctrl', 'alt', 'left')
                    print('已切换到上一首歌!')
                    sleep(2)
                #暂停歌曲
                elif result == '数字5':
                    #添加语音文本
                    #engine.say('歌曲播放即将暂停!')
                    engine.say('OK!The song is about to pause')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    
                    pyautogui.hotkey('ctrl', 'alt', 'p')
                    print('歌曲播放已暂停!')
                    sleep(2)
                #播放歌曲
                elif result == '拳头':
                    #添加语音文本
                    engine.say('OK!The song playing will start soon')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    
                    pyautogui.hotkey('ctrl', 'alt', 'p')
                    print('歌曲播放已开启!')
                    sleep(2)
                #开启或关闭歌词
                elif result == '比心':
                    #添加语音文本
                    #engine.say('已操作歌词显示')
                    engine.say('OK!Operated lyrics display now')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    pyautogui.hotkey('ctrl', 'alt', 'd')
                    print('已开启或关闭歌词显示!')
                    sleep(3)
                elif result == 'OK':
                    #添加语音文本
                    #engine.say('OK,即将休息50秒!')
                    engine.say('About to rest for 50 seconds')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    print('即将休息50秒')
                    sleep(50)
                    #添加语音文本
                    engine.say('Ok!50 seconds passed now')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                elif result == "双手比心":
                    pyautogui.hotkey('ctrl', 'alt', 'l')
                    print('已添加到我喜欢的音乐')
                    #添加语音文本
                    engine.say('OK!Songs have been added to my favorite music')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    sleep(2)
                elif result == "掌心向上":
                    pyautogui.hotkey('ctrl', 'alt', 'down')
                    lower()
                    print('音量已减小')
                    #添加语音文本
                    engine.say('OK!The volume has decreased')
                    #运行,每当要运行说话,都需要下面这个代码
                    engine.runAndWait()
                    sleep(2)
                elif result == "祈祷":
                    pyautogui.hotkey('ctrl', 'alt', 'up')
                    higher()
                    print('音量已加大')
                    #添加语音文本
                    engine.say('OK!The volume has increased')
                    #运行,每当要运行说话,都需要代码
                    engine.runAndWait()
                    sleep(2)
        #捕获代理异常的错误
        except requests.exceptions.ProxyError:
            print('代理服务器错误')
            #添加语音文本
            #engine.say('发生代理服务器错误,正在处理')
            engine.say('The proxy server error occurred,processing now,please wait')
            #运行,每当要运行说话,都需要下面这个代码
            engine.runAndWait()
            close() #关闭代理按钮
            #添加语音文本
            engine.say('Done now')
            #运行,每当要运行说话,都需要下面这个代码
            engine.runAndWait()
        except Exception as e:
            print('手势识别失败,失败的原因是:',type(e).__name__)
            engine.say('There is someing wrong with the'+type(e).__name__)
            engine.runAndWait()
            #clear()
            sleep(2)
        #except ConnectionError:
        if cv.waitKey(1) == 27:
            sys.exit()
            break

#启动函数
if __name__ == "__main__":
    gesture_recognition()


""" 调用手势识别 """
#result = client.gesture(image)
#print(result)
 
