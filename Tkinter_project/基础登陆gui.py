from tkinter import *

def register():
    user = userNameEntry.get()
    pwd = pwdEntry.get()
    t1 = len(user)
    t2 = len(pwd)
    if user == "zhangsan" and pwd == "123":
        statusLabel['text'] = "登录成功"
    else:
        statusLabel['text'] = "用户名或密码错误"
        userNameEntry.delete(0,t1)
        pwdEntry.delete(0,t2)


app = Tk()
userName = Label(app,text = "用户名")
userName.grid(row = 0 , column = 0, sticky = W)

userNameEntry = Entry(app)
userNameEntry.grid(row = 0, column = 1 , sticky = E)

pwd = Label(app, text = "密码")
pwd.grid(row = 1,column = 0,sticky = W)

pwdEntry = Entry(app)
pwdEntry['show'] = '*'
pwdEntry.grid(row = 1, column = 1, sticky = E)

loginBtn = Button(app,text = "登录",command = register)
loginBtn.grid(row = 2, column = 1,sticky = E)

statusLabel = Label(app,text = '')
statusLabel.grid(row = 3)
app.mainloop()
