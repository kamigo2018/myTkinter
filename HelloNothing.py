import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

class MyNothingView(tk.Toplevel):
    def __init__(self,master):
        # 调用父类的初始化函数。
        # To change:这里的MyNothingView要修改
        super(MyNothingView,self).__init__(master)
        
        # 后续的代码可能会调用到自己，方便实用Toplevel的功能。
        self.top = self
        
        # 这里每个View需要改一下，定为自己要做的事情
        self.top.title("什么也不干")
        tk.Grid.rowconfigure(self.top,0,weight=1)
        tk.Grid.columnconfigure(self.top,0,weight=1)        
        
        # 每个窗体自己定义create
        self.create()
        
    def destroy(self):
        # 用户在这里处理一些收尾工作；
        
        # 这里调用父类的销毁窗体函数。
        # To change:这里的MyNothingView要修改
        super(MyNothingView,self).destroy()      

    def __del__(self):
        # 在销毁对象时，进行一些操作，
        # 这个销毁对象可能是由垃圾回收机制触发的。
        pass
  
    def create(self):
        # 创建菜单栏
        self.createMenu()
        
        # 一个A Frame
        #self.createAXXFrame()
        
        # 一个B Frame
        #self.createBXXFrame()

    
    def createMenu(self):
        self.menuBar = tk.Menu()
        # menuBar的父窗体就变成了top。
        self.top.config(menu=self.menuBar)
        
        # 文件菜单
        # tearoff,默认为True,这时菜单栏中有一条虚线，点击虚线，可以将菜单弹出。
        self.fileMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="文件", menu = self.fileMenu)        
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="结束",command = self.top.destroy)        
        
        # 帮助菜单
        self.helpMenu = tk.Menu(self.menuBar,tearoff=False)
        self.menuBar.add_cascade(label="其他", menu = self.helpMenu)
        self.helpMenu.add_command(label="说明",command=self.showInfo)


    def showInfo(self):
        # 调用tkinter.messagebox模块中的显示信息对话框
        # To change:这里的message要修改
        tkMessageBox.showinfo(title="说明",message="Hello Nothing!")
    