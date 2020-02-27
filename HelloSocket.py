import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
from myUtil import SimpleDialog
from myUtil import ImageDivider
from myUtil import StrUtil
from myUtil import RandUtil
from tkinter import ttk
import os.path
import socket

import time
import threading

# 这里产生第二个槽点：显示代码和功能代码混在一起，不方便维护，应该想法分开这些代码。

# 遗留一个问题：如何在程序退出时，关闭socket？

class MyUDPViewer():
    def __init__(self,master):
        # 这个init就是我以后的套路，
        # 产生一个toplevel组件，用来展示一个单独的功能窗体。
        # 调用create()，组织窗体内部的组件
        self.master = master        
        self.top = tk.Toplevel(self.master)
        self.top.title("UDP 演示程序")
        tk.Grid.rowconfigure(self.top,0,weight=1)
        tk.Grid.columnconfigure(self.top,0,weight=1)        
        
        self.ServerRunningFlag = False
        
        # 客户端需要用到的变量
        self.ClientInitalFlag = False
        self.ClientUDPSocket = None
        self.ClientUDPAddr  = ()
        
        # 每个窗体自己定义create
        self.create()
    
    def create(self):
        # 创建菜单栏
        self.createMenu()
        
        # 服务器的Frame
        self.createUDPServerFrame()
        
        # 客户端的Frame
        self.createUDPClientFrame()
    
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
        tkMessageBox.showinfo(title="说明",message="Hello UDP!")
    
    def createUDPServerFrame(self):
        self.UDPServerFrame = tk.Frame(self.top)
        # UDPServerFrame 有两行一列，分别是一个配置frame，一个显示frame
        # 所以这显示frame所在的第二行可以随窗体扩大。
        self.UDPServerFrame.grid_columnconfigure(0, weight=1)
        self.UDPServerFrame.grid_rowconfigure(1, weight=1)
        # UDPServerFrame 在top的第一行第一列
        self.UDPServerFrame.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        
        # 这是一个输入配置参数的frame，里面包括提示符，输入框，按键。
        self.UDPServerConfigFrame = tk.Frame(self.UDPServerFrame)
        self.UDPServerConfigFrame.grid(row = 0,column = 0,sticky=tk.N+tk.S+tk.E+tk.W)        
        self.fillUDPServerConfigFrame()
        
        # 第二个frame，用来展示服务器收到的消息
        self.UDPServerReceivedInfoFrame = tk.Frame(self.UDPServerFrame)
        self.UDPServerReceivedInfoFrame.grid(row = 1,column = 0,sticky=tk.N+tk.S+tk.E+tk.W)    
        self.createUDPServerReceivedInfoFrame()
    
    def fillUDPServerConfigFrame(self):
        '''
        填充这个配置窗体
        '''
        # 这里用了空格来调整组件之间的位置。
        self.serIPLabel = tk.Label(self.UDPServerConfigFrame,text=" 服务器地址（本机IP）：")
        self.serIPInputEntry = tk.Entry(self.UDPServerConfigFrame,width=15)
        #字体这里就不配置了,font = self.inputFrameFont)        
        self.serPortLabel = tk.Label(self.UDPServerConfigFrame,text=" 端口（PORT）：")
        self.serSpaceLabel = tk.Label(self.UDPServerConfigFrame,text=" ")
        self.serPortInputEntry = tk.Entry(self.UDPServerConfigFrame,width=6)
        self.serRunButton = tk.Button(self.UDPServerConfigFrame,width=10,relief = 'raised',\
                                         fg = 'green', text = "RUN", command = self.serverRun)
                                        

        self.serStopButton = tk.Button(self.UDPServerConfigFrame,width=10, relief = 'raised',\
                                         fg = 'red',text = "STOP", command = self.serverStop )
        
        self.serLoadButton = tk.Button(self.UDPServerConfigFrame, width=10,relief = 'raised',\
                                         fg = 'blue', text = "LOAD",  command = self.serverLoad )

        self.serIPLabel.grid(row=0,column=1)
        self.serIPInputEntry.grid(row=0,column=2)
        self.serPortLabel.grid(row=0,column=3)
        self.serPortInputEntry.grid(row=0,column=4)
        self.serSpaceLabel.grid(row=0,column=5)
        self.serRunButton.grid(row=0,column=6)
        
        self.serStopButton.grid(row=0,column=8)
        self.serLoadButton.grid(row=0,column=9)
        
    
    def serverRun(self):
        # UDP服务器运行起来，生成socket，接收信息，展示信息
        # 如果正在运行，什么都不做        
        ipStr = self.serIPInputEntry.get()
        portStr = self.serPortInputEntry.get()
        
        self.ServerUDPSocket = self.__createServerUDPSocket(ipStr,portStr)
        
        if self.ServerUDPSocket == None:
            tkMessageBox.showerror(title="错误",message="UDP服务端Socket还未建立")
            return None
        
        self.ServerRunningFlag = True        
        threading.Thread(target=self.taskRun,args=()).start()
        self.serRunButton.config(state='disabled')
        
    def taskRun(self):
        self.__txtAreaOutput("=== Start at {} ===\n".format(StrUtil.getTimeStr()))  
        try:
            while(self.ServerRunningFlag): 
                data, addr = self.ServerUDPSocket.recvfrom(1024)
                infoStr = StrUtil.getTimeStr() +'|' +("IP:{} PORT:{} :消息[{}]".format(addr[0],addr[1],data.decode('utf-8'))) + "\n"
                
                self.__txtAreaOutput(infoStr)                
        except :
            pass

    def __txtAreaOutput(self,infoStr):
        self.serTxtArea.config(state=tk.NORMAL)
        self.serTxtArea.insert(tk.END,infoStr)                
        self.serTxtArea.config(state=tk.DISABLED)
        self.serTxtArea.see(tk.END) # 一直显示最新的一行
        self.serTxtArea.update()
    
    def serverStop(self):
        # 清空IP，port输入框，
        # 设置停止运行标志，
        # 释放掉服务端socket
        # 恢复Run按钮        
        #self.serIPInputEntry.delete(0,tk.END)
        #self.serPortInputEntry.delete(0,tk.END)
        self.__txtAreaOutput("=== Finish at {} ===\n".format(StrUtil.getTimeStr()))  
        self.ServerRunningFlag = False
        self.serRunButton.config(state='normal')
        if self.ServerUDPSocket:
            self.ServerUDPSocket.close()
    
    def serverLoad(self):
        # Todo:这里应该是从文件载入服务器配置
        self.serIPInputEntry.insert(0,'192.168.0.112')
        self.serPortInputEntry.insert(0,'2000')
        pass


    def __createServerUDPSocket(self, ipStr,portStr):
        if self.__isCorrectIPStr(ipStr) == False:
            return None
        if self.__isCorrentPort(portStr) == False:
            return None       
        
        SerUDPSock =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        
        SerUDPSock.bind((ipStr,int(portStr)))
        return SerUDPSock
    
    def createUDPServerReceivedInfoFrame(self):
        # 在UDPServerReceivedInfoFrame这个框架内：
        # 生成一个带有垂直滚动条的文章显示框，不允许编辑。
        tk.Grid.rowconfigure(self.UDPServerReceivedInfoFrame,0,weight=1) 
        tk.Grid.columnconfigure(self.UDPServerReceivedInfoFrame,0,weight = 1)
        
        # 垂直滚动条
        self.serTxtVerScrollbar = tk.Scrollbar(self.UDPServerReceivedInfoFrame, orient=tk.VERTICAL)
        
        # 实例化一个文本显示区域
        self.serTxtArea = tk.Text(self.UDPServerReceivedInfoFrame,  \
                            yscrollcommand=self.serTxtVerScrollbar.set )
        
        self.serTxtVerScrollbar['command'] = self.serTxtArea.yview
        
        self.serTxtArea.grid(row=0,column=0,sticky='NEWS')
        self.serTxtArea.config(state=tk.DISABLED)
        self.serTxtVerScrollbar.grid(row = 0,column=1,sticky='NS')
    
    def createUDPClientFrame(self):
        self.UDPClientFrame = tk.Frame(self.top)
        # UDPClientFrame 有两行一列，分别是一个配置frame，一个输入frame
        # 第二行可以随窗体扩大。
        self.UDPClientFrame.grid_columnconfigure(0, weight=1)
        self.UDPClientFrame.grid_rowconfigure(1, weight=1)
        # UDPClientFrame 在top的第二行第一列
        self.UDPClientFrame.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        
        # 这是一个输入配置参数的frame，里面包括提示符，输入框，按键。
        self.UDPClientConfigFrame = tk.Frame(self.UDPClientFrame)
        self.UDPClientConfigFrame.grid(row = 0,column = 0,sticky=tk.N+tk.S+tk.E+tk.W)        
        self.fillUDPClientConfigFrame()
        
        # 第二个frame，用来输入文字，发送到服务器
        self.UDPClientInputInfoFrame = tk.Frame(self.UDPClientFrame)
        self.UDPClientInputInfoFrame.grid(row = 1,column = 0,sticky=tk.N+tk.S+tk.E+tk.W)    
        self.createUDPClientInputInfoFrame()

    def fillUDPClientConfigFrame(self):
        '''
        填充这个配置窗体
        '''
        # 这里用了空格来调整组件之间的位置。
        self.cliIPLabel = tk.Label(self.UDPClientConfigFrame,text=" 服务器地址（远端服务器IP）：")
        self.cliIPInputEntry = tk.Entry(self.UDPClientConfigFrame,width=15)
             
        self.cliPortLabel = tk.Label(self.UDPClientConfigFrame,text=" 端口（PORT）：")
        self.cliSpaceLabel = tk.Label(self.UDPClientConfigFrame,text=" ")
        self.cliPortInputEntry = tk.Entry(self.UDPClientConfigFrame,width=6)
        self.cliSetButton = tk.Button(self.UDPClientConfigFrame,width=10,relief = 'raised',\
                                         fg = 'green', text = "SET", command = self.clientSet)
                                        
        self.cliClearButton = tk.Button(self.UDPClientConfigFrame,width=10, relief = 'raised',\
                                        fg = 'brown',text = "CLEAR", command = self.clientClear )

        self.cliIPLabel.grid(row=0,column=1)
        self.cliIPInputEntry.grid(row=0,column=2)
        self.cliPortLabel.grid(row=0,column=3)
        self.cliPortInputEntry.grid(row=0,column=4)
        self.cliSpaceLabel.grid(row=0,column=5)
        self.cliSetButton.grid(row=0,column=6)
        self.cliClearButton.grid(row=0,column=7)
    
    def clientClear(self):
        # 清空IP，port输入框
        # 干掉UDP的客户端Socket
        self.cliIPInputEntry.delete(0,tk.END)
        self.cliPortInputEntry.delete(0,tk.END)
        self.ClientInitalFlag = False
        if self.ClientUDPSocket:
            self.ClientUDPSocket.close()
        self.ClientUDPAddr = ()
        
        # 恢复按键为可按下状态
        self.cliSetButton.config(state='normal')
        
    
    def clientSet(self):
        # 根据IP，port建立客户端socket，
        # 禁止再次使用set按键，一会再想如何禁用按键
        ipStr = self.cliIPInputEntry.get()
        portStr = self.cliPortInputEntry.get()
        
        self.ClientUDPSocket = self.__createClientUDPSocket(ipStr,portStr)
        if self.ClientUDPSocket != None:            
            self.ClientInitalFlag = True
            # 我这里有意把地址和socket绑定在一起，
            # 其实udpsocket可以单独产生，然后每次传入对应地址就可以发送接收数据
            self.ClientUDPAddr = (ipStr,int(portStr))            
            self.cliSetButton.config(state='disabled')
            tkMessageBox.showinfo(title="成功",message="UDP客户端socket建立成功")
        else:
            self.ClientInitalFlag = False
            # Todo:这里弹框提示无法产生相应的socket
            tkMessageBox.showerror(title="错误",message="无法建立UDP客户端socket\nIP={}\nPort={}".format(ipStr,portStr))
            
            
            
    def __createClientUDPSocket(self, ipStr,portStr):
        # Todo: 根据ip和port产生一个客户端upd socket，
        
        if self.__isCorrectIPStr(ipStr) == False:
            return None
        if self.__isCorrentPort(portStr) == False:
            return None       
        
        return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
    def __isCorrectIPStr(self,ipStr):
        # Todo:这里还要再看看，如何判断一个字符串是否是合理的ip地址。
        temp = ipStr.split('.')
        if(len(temp)!=4):
            return False
        else:
            for i in temp:
                tempInt = int(i)
                if (tempInt>255 or tempInt<0):
                    return False
        return True
                    

    def __isCorrentPort(self,portStr):
        temp =  int(portStr)
        if (temp<65536 and temp >0):
            return True
        else:
            return False
        
    
    def createUDPClientInputInfoFrame(self):
        self.cliInputLabel = tk.Label(self.UDPClientInputInfoFrame,text=" 输入信息 ：")
        self.cliSpaceLabel1 = tk.Label(self.UDPClientInputInfoFrame,text=" ")
        self.cliInputEntry = tk.Entry(self.UDPClientInputInfoFrame,width=80)
        self.cliSendButton = tk.Button(self.UDPClientInputInfoFrame,width=10,relief = 'raised',\
                                         fg = 'red', text = "SEND", command = self.clientSend)
                                        
        self.cliCancelButton = tk.Button(self.UDPClientInputInfoFrame,width=10, relief = 'raised',\
                                        fg = 'brown',text = "CANCEL", command = self.clientCancel )

        self.cliInputLabel.grid(row=1,column=0)
        self.cliInputEntry.grid(row=1,column=1)
        self.cliSpaceLabel1.grid(row=1,column=2)
        self.cliSendButton.grid(row=1,column=3)
        self.cliCancelButton.grid(row=1,column=4)
        
    def clientSend(self):
        if self.ClientInitalFlag == False:
            tkMessageBox.showerror(title="错误",message="UDP客户端Socket还未建立")
            return None
            
        infoStr = self.cliInputEntry.get()
        # Todo 这里是发送给服务器，要看看服务器接收到了什么
        # print(infoStr)
        msg = infoStr.encode('utf-8')
        self.ClientUDPSocket.sendto(msg,(self.ClientUDPAddr))        
        self.clientCancel()
    
    def clientCancel(self):
        # 清空输入区的文字
        self.cliInputEntry.delete(0,tk.END)
        
        
        
class MyTCPViewer():
    def __init__(self,master):
        # 这个init就是我以后的套路，
        # 产生一个toplevel组件，用来展示一个单独的功能窗体。
        # 调用create()，组织窗体内部的组件                
        self.master = master        
        self.top = tk.Toplevel(self.master)
        self.top.title("TCP 演示程序")
        tk.Grid.rowconfigure(self.top,0,weight=1)
        tk.Grid.columnconfigure(self.top,0,weight=1)
        
        # 每个窗体自己定义create
        #self.create()



