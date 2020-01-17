import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master        
        # https://stackoverflow.com/questions/7591294/how-to-create-a-self-resizing-grid-of-buttons-in-tkinter
        # 这两句是 grid 布局，组件缩放的关键因素：父容器必须要配置这两句，才能实现子容器的缩放。
        tk.Grid.rowconfigure(self.root,0,weight=1)
        tk.Grid.columnconfigure(self.root,0,weight=1)
        
        self.master = tk.Frame(self.root)      
        tk.Grid.rowconfigure(self.master,0,weight=1)
        tk.Grid.columnconfigure(self.master,0,weight=1)        
        self.master.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)        
        
        
        self.create()
        self.imageFlag = 0
        
    
    def create(self):
        '''
        create函数，用来产生相应的应用GUI组件
        
        包括一个菜单栏，一个显示框架，一个输入框架
        '''
        # 定义Master的标题栏
        self.root.title("GUI应用-Tk")
        # 替换应用的图标
        self.root.iconbitmap("sources/blackEight.ico")
        # 设置窗体最小大小，和最大大小：
        #self.root.maxsize(1200,800)
        #self.root.minsize(300,200)
        
        
        # 创建菜单栏
        
        # 创建显示文字的text widget 的Frame
        self.createShowResultFrame()
        
        # 创建输入文字的Frame
        self.createInputFrame()
        
        

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

        self.inputLabel.grid(row=0,column=0,sticky='NWES')
        self.inputEntry.grid(row=0,column=1,columnspan=7,sticky='NWES')
        self.inputSendButton.grid(row = 1,column=6,sticky='NWES')
        self.inputCleanButton.grid(row = 1,column=4,sticky='NWES')
        self.inputRefreshButton.grid(row = 1,column=3,sticky='NWES')        
        self.inputFrame.columnconfigure(2,weight=10)

        self.inputFrame.grid(row=1,column=0,sticky=tk.E+tk.W)  

    def inputSend(self):
        filePath = self.inputEntry.get()
        if len(filePath)==0:
            print("没有输入")
            return
        
        temp = filePath.split('.')        
        if len(temp)>1 and (temp[-1].lower() in ['jpg','png','jpeg']) :
            self.showImage(filePath)
        
        self.inputEntry.delete(0,tk.END)

    
    def inputRefresh(self):
        if self.imageFlag == 0:
            return 
        else:
            print("此处应该重新设置图像大小，重新绘制图像")
            pass

    def inputClean(self):
        if self.imageFlag == 0:
            return 
        else:
            print("清空")
            self.picCanvas.delete(tk.ALL)
            self.imageFlag = 0
        

    def showImage(self, filePath):
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
        
        except Exception:
            print("异常")
            return 
            
            
            
        
        
#================================================
#==================== MAIN ======================
#================================================
if __name__=="__main__":
    root = tk.Tk()                 # 只能有一个tk.Tk()产生一个。
    app = Application(master=root)
    app.mainloop()