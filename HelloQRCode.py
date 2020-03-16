import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
from PIL import ImageTk,Image
import tkinter.filedialog

from myUtil import StrUtil
from CommonFrame import MyShowOneImageFrame
from CommonFrame import MyInputStringFrame

import qrcode
import cv2

# 参考https://blog.csdn.net/weixin_42703239/article/details/104349417

class MyQRCodeView(tk.Toplevel):
    def __init__(self,master):
        
        super(MyQRCodeView,self).__init__(master)

        self.top = self
        
        self.top.title("二维码QR Code演示程序")
        tk.Grid.rowconfigure(self.top,0,weight=1)
        tk.Grid.columnconfigure(self.top,0,weight=1)
        
        # 每个窗体自己定义create
        self.create()

    def destroy(self):
        # 用户在这里处理一些收尾工作；
        # 这里调用父类的销毁窗体函数。
        super(MyQRCodeView,self).destroy()
        
    def __del__(self):
        # 在销毁对象时，进行一些操作，
        # 这个销毁对象可能是由垃圾回收机制触发的。
       
        pass

    def create(self):
        # 一个A Frame
        self.createShowQRCodeImageFrame()
        
        # 一个B Frame
        self.createCreateQRCodeFrame()
        
        # 创建菜单栏，
        # 为了在工具栏中调用子框架的功能，所以等生成子框架后才创建菜单栏
        self.createMenu()
    
    
    def createMenu(self):
        self.menuBar = tk.Menu()
        # menuBar的父窗体就变成了top。
        self.top.config(menu=self.menuBar)
        
        # 文件菜单
        # tearoff,默认为True,这时菜单栏中有一条虚线，点击虚线，可以将菜单弹出。
        self.fileMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="文件", menu = self.fileMenu)
        self.fileMenu.add_command(label="打开图片",command = self.openImage)  
        self.fileMenu.add_command(label="图片另存为",command = self.saveAs)        
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="结束",command = self.top.destroy)        

        # 操作菜单
        self.operationMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="操作", menu = self.operationMenu)
        self.operationMenu.add_command(label="适应画布",command = self.myQRCodeImageViewFrame.refresh)
        self.operationMenu.add_separator()
        self.operationMenu.add_command(label="清空画布",command = self.clean)   
        self.operationMenu.add_separator()
        self.operationMenu.add_command(label="识别二维码",command = self.decode)
        
        # 帮助菜单
        self.helpMenu = tk.Menu(self.menuBar,tearoff=False)
        self.menuBar.add_cascade(label="其他", menu = self.helpMenu)
        self.helpMenu.add_command(label="说明",command=self.showInfo)


    def showInfo(self):
        # 调用tkinter.messagebox模块中的显示信息对话框
        # To change:这里的message要修改
        tkMessageBox.showinfo(title="说明",message="Hello QRCod! 2020-03-09")
    
    def createShowQRCodeImageFrame(self):
        # 这个和功能一，展示图片中的窗体功能一致，所以尽可能拷贝。
        ## Todo：这里发现，第一次写的展示图片的功能有可能复用，
        ##      所以考虑将这个功能优化，或者独立出来。应该会节省以后的工作
        ## 这块的功能是：
        ##  1、一个Frame，嵌入一个canvas，用来展示图片。
        ##  2、Frame带有滚动条，如果图片大小超出canvas的大小，可以通过滚动条查看图片；
        ##  3、最好带有放大，缩小，适应canvas大小，复位的功能键。这些功能键在没有图片时，可隐藏。
        ##  4、可以传入文件名，或者Image对象，触发展示图片；
        ##一个疑问，这个Frame怎么其他组件进行交互？
        
        # 这里要一个能够展示二维码图像的框体
        self.myQRCodeImageViewFrame = MyShowOneImageFrame(self.top)
        self.myQRCodeImageViewFrame.setGrid(0,0) # 将这个Frame设置在0行，0列
        pass

    def createCreateQRCodeFrame(self):
        self.myQRCodeInputViewFrame = MyInputStringFrame(self.top)
        self.myQRCodeInputViewFrame.setGrid(0,1)
    
    def subFrameCallHandler(self,messageInfo,strInfo):
        if messageInfo == 'NEW_QRCODE': # 子框架中有事情要告诉父框架。这里是子框架产生了二维码。
            # print("输入字符[{}]".format(data))  #这个data会自带一个换行符"\n"
            data = strInfo[:-1]
            if len(data) == 0:
                tkMessageBox.showinfo(title="说明",message="无输入字符，不生成二维码")
                return
            else:
                tempFile = qrcode.make(data)
                tempFile.save('tmp/qrcode.jpg')

            image = Image.open('tmp/qrcode.jpg')
            self.myQRCodeImageViewFrame.showImage(image)
    
    def openImage(self):
        fileName = tkinter.filedialog.askopenfilename(defaultextension=".*",\
            filetypes=[('jpg', '.jpg'), ('png', '.png'),('jpeg','jpeg'),('all files', '.*')])
        tempList = fileName.split(".")
        if tempList[-1].lower() in ['jpg','png','jpeg']:
            image = Image.open(fileName)
            self.myQRCodeImageViewFrame.showImage(image)
        else:
            tkMessageBox.showinfo(title="提示",message="只能打开图片文件，无法打开其他文件")
    
    def saveAs(self):
        if self.myQRCodeImageViewFrame.imageFlag == 1:
            image = self.myQRCodeImageViewFrame.image
            # 弹出对话框，选择保存的文件，文件名
            # http://codingdict.com/sources/py/tkinter.filedialog/13817.html
            newFileName = tkinter.filedialog.asksaveasfilename(defaultextension=".jpg",\
            filetypes=[('image files', '.jpg'), ('all files', '.*')])            
            # 保存文件
            image.save(newFileName) 
        else:
            print("没有图片需要保存")
    
    def clean(self):
        self.myQRCodeImageViewFrame.clean()
    
    def decode(self):
        '''
        识别二维码有多重方式，
        https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
        我学习的是下面这个：
        https://www.thepythoncode.com/article/generate-read-qr-code-python
        '''
        if self.myQRCodeImageViewFrame.imageFlag == 1:
            fileName  = "tmp/decode.jpg" 
            image = self.myQRCodeImageViewFrame.image
            image.save(fileName) # 先把他存成临时文件，给cv2用
            
            # cv2读入图片数据
            img = cv2.imread(fileName)
            
            # 初始化一个二维码解码器
            detector = cv2.QRCodeDetector()
            
            # 识别二维码
            data, bbox, straight_qrcode = detector.detectAndDecode(img)
            
            # 如果有二维码，将二维码区域识别画出来
            if bbox is not None:
                self.myQRCodeInputViewFrame.txtArea.insert(0.0,data)
                n_lines = len(bbox)
                for i in range(n_lines):
                    # draw all lines
                    point1 = tuple(bbox[i][0])
                    point2 = tuple(bbox[(i+1) % n_lines][0])
                    # bbox 是这个二维码的四个顶点，用红线将二维码框起来。
                    
                    cv2.line(img, point1, point2, color=(0, 0, 255), thickness=5)
                    cv2.imwrite(fileName,img)
                    image = Image.open(fileName)
                    self.myQRCodeImageViewFrame.showImage(image)
            else:
                tkMessageBox.showinfo(title="提示",message="未识别到二维码")
        