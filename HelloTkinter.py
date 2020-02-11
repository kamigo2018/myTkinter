import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
from myUtil import SimpleDialog
from myUtil import ImageDivider
from tkinter import ttk
import os.path

from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # root 是个Tk, 根容器，可以添加菜单栏
        self.root = master        
        # https://stackoverflow.com/questions/7591294/how-to-create-a-self-resizing-grid-of-buttons-in-tkinter
        # 这两句是 grid 布局，组件缩放的关键因素：父容器必须要配置这两句，才能实现子容器的缩放。
        tk.Grid.rowconfigure(self.root,0,weight=1)
        tk.Grid.columnconfigure(self.root,0,weight=1)
        
        # master 是个Frame他不能添加菜单；
        self.master = tk.Frame(self.root)      
        tk.Grid.rowconfigure(self.master,0,weight=1)
        tk.Grid.columnconfigure(self.master,0,weight=1)        
        self.master.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)        
        
        self.imageResizeRatio = 100
        self.imageFlag = 0
        self.create()
        
   
    def create(self):
        '''
        create函数，用来产生相应的应用GUI组件
        
        包括一个菜单栏，一个显示框架，一个输入框架
        '''
        # 定义Master的标题栏
        self.root.title("GUI应用-Tk")
        # 替换应用的图标
        self.root.iconbitmap("D:/git_repo/myTkinter/sources/blackEight.ico")
        # 设置窗体最小大小，和最大大小：
        #self.root.maxsize(1200,800)
        #self.root.minsize(300,200)
        
        
        # 创建菜单栏
        self.createMenu()
        
        # 创建显示文字的text widget 的Frame
        self.createShowResultFrame()
        
        # 创建输入文字的Frame
        self.createInputFrame()

       
    def createMenu(self):
        self.menuBar = tk.Menu()
        self.root.config(menu=self.menuBar)
        
        # 文件菜单
        # tearoff,默认为True,这时菜单栏中有一条虚线，点击虚线，可以将菜单弹出。
        self.fileMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="文件", menu = self.fileMenu)
        self.fileMenu.add_command(label="打开",command=self.openImageFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="结束",command = self.root.quit)
        
        # 小功能菜单
        self.functionMenu = tk.Menu(self.menuBar,tearoff=False)
        self.menuBar.add_cascade(label="功能", menu = self.functionMenu)
        self.functionMenu.add_command(label="分格",command=self.divideImage)
        
        # 帮助菜单
        self.helpMenu = tk.Menu(self.menuBar,tearoff=False)
        self.menuBar.add_cascade(label="其他", menu = self.helpMenu)
        self.helpMenu.add_command(label="说明",command=self.showInfo)
    

    def showInfo(self):
        # 调用tkinter.messagebox模块中的显示信息对话框
        tkMessageBox.showinfo(title="说明",message="hello")
        

    def openImageFile(self):
        filePath = tkFileDialog.askopenfilename(title="打开文件")
        if len(filePath)==0:
            #print("没有输入")
            return
        
        temp = filePath.split('.')        
        if len(temp)>1 and (temp[-1].lower() in ['jpg','png','jpeg']) :
            self.showImage(filePath)
    

    def divideImage(self):
        if self.imageFlag == 0:
            tkMessageBox.showinfo(title="提示", \
                    message="先打开一张图片，再进行分格")
            return        
        
        dialog = SimpleDialog(self.root)
        self.root.wait_window(dialog.top)
        rowNumber,columnNubmer = dialog.getInput()
        rowNumber = int(rowNumber)
        columnNubmer = int(columnNubmer)
        imageDivider = ImageDivider()
        self.newImage = imageDivider.divide(self.image,rowNumber,columnNubmer)
        # 调用系统工具，查看图片
        self.newImage.show()
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        # 这儿其实可以随机生成一个文件名字，为了简单就弄个1.jgp
        self.newImage.save('tmp\\1.jpg','JPEG')
       
       
    def createShowResultFrame(self):
        '''
        创建一个结果展示框，先显示一张图片，这样可以给这个框架占住位置
        '''
        self.showResultFrame = tk.Frame(self.master) #创建一个Frame，指定他的父容器是我们的根窗体
        self.showResultFrame.config(borderwidth = 2, relief = 'ridge')

        
        self.picCanvasHorScrollbar = \
            tk.Scrollbar(self.showResultFrame, orient=tk.HORIZONTAL)
        self.picCanvasVerScrollbar = \
            tk.Scrollbar(self.showResultFrame, orient=tk.VERTICAL)        
        
        self.picCanvas = tk.Canvas(self.showResultFrame, \
                            scrollregion=(0, 0, 1000, 1000), \
                            yscrollcommand=self.picCanvasVerScrollbar.set, \
                            xscrollcommand=self.picCanvasHorScrollbar.set )
                            
        self.picCanvasHorScrollbar['command'] =  self.picCanvas.xview                  
        self.picCanvasVerScrollbar['command'] =  self.picCanvas.yview 

        # Bottom-right corner resize widget
        #self.sizegrip = ttk.Sizegrip(self.showResultFrame)
        #self.sizegrip.grid(column=1, row=1, sticky=(tk.S,tk.E))
        
        self.picCanvas.grid(column=0, row=0, sticky='NWES')
        self.picCanvasHorScrollbar.grid(column=0, row=1, sticky=(tk.W,tk.E))
        self.picCanvasVerScrollbar.grid(column=1, row=0, sticky=(tk.N,tk.S))
        
        self.showResultFrame.grid_columnconfigure(0, weight=1)
        self.showResultFrame.grid_rowconfigure(0, weight=1)
        '''
        weight给这个参数设置一定的数值（权重），
        就能够使该列或行以此权重，在多余的空间中伸缩，平铺。
        比如，w 插件使用了 grid 布局，并且有这两行代码： 
        w.columnconfigure(0, weight=3) 
        w.columnconfigure(1, weight=1) 
        这会将多余的 3/4 空间分配给第一列，其余的1/4空间分配给第二列。
        如果没有使用此option，就不会伸缩行或列。
        '''

        self.showResultFrame.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)  

   
    def createInputFrame(self):
        '''
        创建一个输入框，几个按钮
        '''
        self.inputFrameFont = tkFont.Font(family='微软雅黑',size = '16')
        self.inputFrame = tk.Frame(self.master) 
        self.inputFrame.config(borderwidth = 4, \
                               relief = 'ridge' )
        
        self.inputLabel = tk.Label(self.inputFrame, \
                                   font = self.inputFrameFont,\
                                   text="输入内容:")
       
        self.inputEntry = tk.Entry(self.inputFrame,font = self.inputFrameFont)
        
        
        self.inputSendButton = tk.Button(self.inputFrame,\
                                         font = self.inputFrameFont, \
                                         width=8,\
                                         text = "发送", \
                                         command = self.inputSend \
                                        )
        self.inputRefreshButton = tk.Button(self.inputFrame,\
                                         font = self.inputFrameFont, \
                                         width=8,\
                                         fg = 'green',\
                                         text = "刷新", \
                                         command = self.inputRefresh \
                                        )
        
        self.inputCleanButton = tk.Button(self.inputFrame,\
                                         font = self.inputFrameFont, \
                                         width=8,\
                                         fg = 'red',\
                                         text = "清空", \
                                         command = self.inputClean \
                                        )

        self.imageZoomIn = tk.PhotoImage(file='D:/git_repo/myTkinter/sources/放大.png')
        self.inputZoomInButton = tk.Button(self.inputFrame,\
                                         image = self.imageZoomIn, \
                                         command = self.zoomIn  )

        self.imageZoomOut = tk.PhotoImage(file='D:/git_repo/myTkinter/sources/缩小.png')
        self.inputZoomOutButton = tk.Button(self.inputFrame,\
                                         image = self.imageZoomOut, \
                                         command = self.zoomOut  )
        
        self.inputLabel.grid(row=0,column=0,sticky='NWES')
        self.inputEntry.grid(row=0,column=1,columnspan=10,sticky='NWES')
        self.inputSendButton.grid(row = 1,column=9,columnspan=2,sticky='NWES')
        self.inputCleanButton.grid(row = 1,column=7,columnspan=2,sticky='NWES')
        self.inputRefreshButton.grid(row = 1,column=5,columnspan=2,sticky='NWES')        
        
        # 这是初始化，所以永远执行不到这个if分支里面去，有这两句话，是因为写代码时遗留下来，不想删除，所以加了if条件。
        if self.imageFlag ==1:
            self.inputZoomInButton.grid(row=1,column=3,sticky='NWES')  
            self.inputZoomOutButton.grid(row=1,column=4,sticky='NWES')
        
        self.inputFrame.columnconfigure(2,weight=10)

        self.inputFrame.grid(row=1,column=0,sticky=tk.E+tk.W)  


    def zoomIn(self):
        self.imageResizeRatio += 3
        
        #print("此处应该重新设置图像大小，重新绘制图像")
        winX = self.picCanvas.winfo_width()
        winY = self.picCanvas.winfo_height()
        (x,y) = self.image.size
        newY = int(y*self.imageResizeRatio/100)
        newX = int(x*self.imageResizeRatio/100)
        self.newImage = self.image.resize((newX,newY), Image.ANTIALIAS)
            
        self.picCanvasImage = ImageTk.PhotoImage(self.newImage)
        #self.picCanvas ['scrollregion']=(0, 0, newX, newY)
        # 将新生成的图像的中心，放在画布的中心，从而确定滚动条的位置：
        # 需要画个图，用newX，winX表示一下，就能得到下面的关系
        self.picCanvas ['scrollregion']=( int((winX-newX)/2), int((winY-newY)/2), winX-int((winX-newX)/2) , winY-int((winY-newY)/2))
        self.picCanvas.create_image(winX/2,winY/2,image = self.picCanvasImage)
        self.imageFlag = 1


    def zoomOut(self):
        self.imageResizeRatio -= 3
        
        #print("此处应该重新设置图像大小，重新绘制图像")
        winX = self.picCanvas.winfo_width()
        winY = self.picCanvas.winfo_height()
        
        (x,y) = self.image.size
        
        newY = int(y*self.imageResizeRatio/100)
        newX = int(x*self.imageResizeRatio/100)
        self.newImage = self.image.resize((newX,newY), Image.ANTIALIAS)
        
        self.picCanvasImage = ImageTk.PhotoImage(self.newImage)
        #self.picCanvas ['scrollregion']=(0, 0, newX, newY)
        # 将新生成的图像的中心，放在画布的中心，从而确定滚动条的位置：
        # 需要画个图，用newX，winX表示一下，就能得到下面的关系
        self.picCanvas ['scrollregion']=( int((winX-newX)/2), int((winY-newY)/2), winX-int((winX-newX)/2) , winY-int((winY-newY)/2))
        self.picCanvas.create_image(winX/2,winY/2,image = self.picCanvasImage)
        self.imageFlag = 1


    def inputSend(self):
        filePath = self.inputEntry.get()
        if len(filePath)==0:
            #print("没有输入")
            return
        
        temp = filePath.split('.')        
        if len(temp)>1 and (temp[-1].lower() in ['jpg','png','jpeg']) :
            self.showImage(filePath)
        
        self.inputEntry.delete(0,tk.END)


    def inputRefresh(self):
        if self.imageFlag == 0:
            return 
        else:
            #print("此处应该重新设置图像大小，重新绘制图像")
            winX = self.picCanvas.winfo_width()
            winY = self.picCanvas.winfo_height()
            
            (x,y) = self.image.size
            
            if winX > winY:
                # 画布的宽大于高，先紧着高，把高度填满
                newY = winY
                newX = int(x*winY/y)
                self.imageResizeRatio = int(winY*100/y)
            else:
                # 先把宽填满
                newX = winX
                newY = int(y*winX/x)
                self.imageResizeRatio = int(winX*100/x)
            
            self.newImage = self.image.resize((newX,newY), Image.ANTIALIAS)
            # 这里为什么不将image重新幅值？因为如果缩小了，再放大，图像就模糊了。
            # self.image = self.newImage 
            self.picCanvasImage = ImageTk.PhotoImage(self.newImage)
            self.picCanvas ['scrollregion']=(0, 0, newX, newY)
            self.picCanvas.create_image(winX/2,winY/2,image = self.picCanvasImage)
            self.imageFlag = 1


    def inputClean(self):
        if self.imageFlag == 0:
            return 
        else:
            #print("清空")
            self.picCanvas.delete(tk.ALL)
            self.imageFlag = 0
            self.inputZoomInButton.grid_forget()  
            self.inputZoomOutButton.grid_forget()


    def showImage(self, filePath):
        # 将图像的左上角顶点放在画布的左上角顶点。后续其他显示图片的方法都是将图片的中心点，放在画布的中心点。
        try:            
            # https://jingyan.baidu.com/article/b7001fe1d836310e7282dd00.html
            # 百度经验教我怎么获取画布大小
            #x = self.picCanvas.winfo_width()            
            #y = self.picCanvas.winfo_height()
            #print("画布大小为：",(x,y))            
            #self.image = self.origImage.resize((int(x*95/100),int(y*95/100)),Image.ANTIALIAS)
            
            self.image = Image.open(filePath)
            (x,y) = self.image.size            
            self.picCanvasImage = ImageTk.PhotoImage(self.image)
            #print("图像大小为：",(x,y))
            
            self.picCanvas ['scrollregion']=(0, 0, x, y)            
            
            # 这个create_image的前两个参数，图片的位置（position）：
            # 应该说的是将image图片的中心点，放在画布的什么位置
            self.picCanvas.create_image(x/2,y/2,image = self.picCanvasImage)
            self.imageFlag = 1
            
            self.inputZoomInButton.grid(row=1,column=3,sticky='NWES')  
            self.inputZoomOutButton.grid(row=1,column=4,sticky='NWES')
        except Exception:
            #print("异常")
            return


#================================================
#==================== MAIN ======================
#================================================
if __name__=="__main__":
    root = tk.Tk()                 # 只能有一个tk.Tk()产生一个。
    app = Application(master=root)
    app.mainloop()
# 打包遇到的一个问题： https://blog.csdn.net/gdkyxy2013/article/details/103755124