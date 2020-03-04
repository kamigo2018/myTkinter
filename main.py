
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from HelloTkinter import MyImageViewer
from HelloSocket import MyUDPViewer
from HelloSocket import MyTCPViewer

class Application(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        
        root = self.root = master
        root.iconbitmap("./sources/blackEight.ico")
        root.title("GUI应用-Tk")
        root.geometry( '200x460')
        root.resizable(0,1)
        root.config(bg="steelblue")
        
        self.create()
        
    def create(self):        
        '''
        将主界面设计成一个竖条形状，分成两个区域：自主研发功能区+退出按键区。
        自主研发功能区：目前里面放置多个功能按键，后续按下每一个按键弹出一个界面。
        退出按键区：就放置一个按键，用来退出。
        '''
        self.frameFont = tkFont.Font(family='微软雅黑',size = '16')
        
        # 整个区域划分成两个窗体，一个用来放功能按键，一个专门用来放退出按键。
        # 我还想给这个中间加条线。现在还不会。不过应该可以加，如何能让他明显一点？
        self.funcFrame = tk.Frame(self.root);
        self.separatorLine = ttk.Separator(self.root,orient='horizontal',style='red.TSeparator')
        self.quitFrame = tk.Frame(self.root);
        
        # ==start==
        # 设置上面两部分区域的框架，容纳其他显示在顶层页面的组件
        self.funcFrame.grid(row = 0, column=0, sticky='NWES')
        self.separatorLine.grid(row = 1, column=0, sticky='NWES') # 这条分割线没有显示出来，没起作用？
        self.quitFrame.grid(row = 2, column=0, sticky='NWES')
        
        tk.Grid.rowconfigure(self.root,0,weight=15)
        # tk.Grid.rowconfigure(self.root,1,weight=15) #还是看不到这条线
        tk.Grid.rowconfigure(self.root,2,weight=1) # 甚至应该考虑这个窗体是否应该固定大小
        tk.Grid.columnconfigure(self.root,0,weight = 1)
        # ==end==
        
        # 实例化在funcFrame里面的4个函数按键
        self.button1 = tk.Button(self.funcFrame,text='显示图片',font=self.frameFont, command = self.func1)
        self.button2 = tk.Button(self.funcFrame,text='UDP程序',font=self.frameFont, command = self.func2)
        self.button3 = tk.Button(self.funcFrame,text='TCP程序',font=self.frameFont, command = self.func3)
        self.button4 = tk.Button(self.funcFrame,text='还没想好',font=self.frameFont, command = self.func4)
        
        # ==start==
        # 设置以上4个按键的位置
        self.button1.grid(row=0,column=0,rowspan=1,sticky='NWES')
        self.button2.grid(row=1,column=0,rowspan=1,sticky='NWES')
        self.button3.grid(row=2,column=0,rowspan=1,sticky='NWES')
        self.button4.grid(row=3,column=0,rowspan=1,sticky='NWES')
        
        tk.Grid.rowconfigure(self.funcFrame,0,weight=1)
        tk.Grid.rowconfigure(self.funcFrame,1,weight=1)
        tk.Grid.rowconfigure(self.funcFrame,2,weight=1)
        tk.Grid.rowconfigure(self.funcFrame,3,weight=1)
        
        tk.Grid.columnconfigure(self.funcFrame,0,weight=1)
        # ==end==
        
        # 实例化一个退出按键
        self.buttonQuit = tk.Button(self.quitFrame,text='退 出',font=self.frameFont)       
        self.buttonQuit.config(bg='gray',fg='black',command=self.quit)
        
        # ==start==
        # == 设置quitFrame中按键的大小和位置 ==
        self.buttonQuit.grid(row=0,column=0,sticky='NWES')
        tk.Grid.rowconfigure(self.quitFrame,0,weight=1)        
        tk.Grid.columnconfigure(self.quitFrame,0,weight=1)        
        # ==end==
        pass
        


    def quit(self):
        # self.root.quit()
        self.root.destroy() # 这两个有什么区别？
    
    def func1(self):
        # 这里需要隐藏主界面，弹出对应功能界面。操作完成后，退出功能界面，回到主界面。
        # 保存原始窗体的大小，参考：
        # https://www.daniweb.com/programming/software-development/threads/322818/tkinter-window-size
        # https://www.imooc.com/wenda/detail/608947 
        
        # 主窗体的宽高尺寸
        winWidth = self.root.winfo_width()
        winHeight = self.root.winfo_height()
        
        # 主窗体在屏幕的位置
        screenX = self.root.winfo_x()
        screenY = self.root.winfo_y()
        
        self.root.withdraw()        
        
        myImageViewer = MyImageViewer(self.root)
        self.root.wait_window(myImageViewer.top)
        
        self.root.deiconify()
        self.root.update()        
        self.root.geometry(("{}x{}+{}+{}").format(winWidth,winHeight,screenX,screenY))
        
    def func2(self):
        # 主窗体的宽高尺寸
        winWidth = self.root.winfo_width()
        winHeight = self.root.winfo_height()
        
        # 主窗体在屏幕的位置
        screenX = self.root.winfo_x()
        screenY = self.root.winfo_y()
        
        self.root.withdraw()        
        
        myUDPViewer = MyUDPViewer(self.root)
        self.root.wait_window(myUDPViewer.top)
        
        self.root.deiconify()
        self.root.update()        
        self.root.geometry(("{}x{}+{}+{}").format(winWidth,winHeight,screenX,screenY))
        
        #print("UDP")
        #https://www.studytonight.com/network-programming-in-python/networking-terminologies
   
    def func3(self):
        pass
        #print("TCP")
        
    def func4(self):        
        # 使用withdraw和update，deiconify是一种隐藏主窗口的方法
        # 能不能在toplevel的创建和结束时调用隐藏主窗口？
        #
        self.root.withdraw()
        
        #assistantJarvis = Jarvis(self.root)
        #self.root.wait_window(assistantJarvis.top)
        
        #self.root.wait_window(MyImageViewer(self.root).top)
        
        #self.root.update()
        self.root.deiconify()
        
'''
1, 是否需要加上logging？
2，多文件处理。
'''


if __name__== "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
# 打包遇到的一个问题： https://blog.csdn.net/gdkyxy2013/article/details/103755124
    