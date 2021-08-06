from tkinter import  *
import pymysql  #连接数据库

#绑定的打印和并保存至数据库的函数
def printLog():
    #获取三个提交的信息
    id = id_str.get()
    name = name_str.get()
    introduce = introduce_text.get('0.0',END) #获取Text的内容get需要两个参数,

    #打印提交信息在Text日志中
    info = id+'\n'+name+'\n'+introduce
    txt.insert(END,info)

    """保存信息到mydb数据库中的student_infos数据表中"""
    # 使用pymysql.connect方法连接数据库
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='260957', database='mydb', charset='utf8')
    # 操作数据库，获取db下的cursor对象
    cursor = db.cursor()
    # 使用cursor.execute来执行SQL语句
    # 提交表单内条写入数据库
    sql = "insert into student_infos(id,name,introduction) values(%s,%s,%s)"
    cursor.execute(sql,(id,name,introduce))
    # 提交数据至数据库
    db.commit()
    db.close()

    #提交后清空三个文本框
    id_entry.delete(0,END)
    name_entry.delete(0,END)     #注意如果是Entry的输入框的清空的话，第一个直接0就可以
    introduce_text.delete('0.0',END) #注意如果是Text的输入框的清空的话，第一个需是'0.0'字符串形式，0.0表示第0行第0列

#初始化主窗口和大小
root = Tk()
root.title('信息提交器')
root.geometry('400x300')

#添加一个标签信息
lb = Label(root,text = '请输入您的个人信息:',font=('Arial', 14))
lb.pack(side = 'top')

#添加学号标签
id = Label(root,text = '学号:')
id.place(relx = 0.16,rely = 0.1)

#添加姓名标签
name = Label(root,text='姓名:')
name.place(relx = 0.16,rely = 0.2)

#添加学号输入框
id_str = StringVar()
id_str.set('如:123456789')
id_entry = Entry(root,textvariable=id_str)
id_entry.place(relx = 0.25,rely = 0.11)

#添加姓名输入框
name_str = StringVar()
name_entry = Entry(root,textvariable = name_str)
name_entry.place(relx = 0.25,rely  = 0.21)

#添加间接标签
introduce = Label(root,text = '简介:')
introduce.place(relx = 0.16,rely = 0.3)

#添加简介的文本输入框
introduce_text = Text(root,width = 38,height = 7)
introduce_text.place(relx = 0.25,rely = 0.31)

#创建提交按钮
button = Button(root,text = '确认提交',command = printLog)
button.place(relx = 0.7,rely = 0.10)

#创建文本框显示输入的结果
txt = Text(root)
txt.place(relx = 0,rely = 0.69)

#创建退出按钮
button2 = Button(root,text = '退出程序',command = root.destroy)
button2.place(relx = 0.7,rely = 0.20)
root.mainloop()