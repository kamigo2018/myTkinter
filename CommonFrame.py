'''
这里应该是一些通用框架
1、ShowImageFrame 展示图片框架的基类
'''
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk,Image
from tkinter import ttk
import tkinter.messagebox as tkMessageBox


'''
ShowImageFrame 是展示图片这个框体的基类
用来生成一个Frame框架，里面包含一个canvas画布，
一个水平滚动条，一个垂直滚动条。
不包含其他展示图片，清除展示图片，放大图片，缩小图片的功能。
'''
class ShowImageFrame(tk.Frame):
    def __init__(self,master):
        super(ShowImageFrame,self).__init__(master)
        # 记住父容器是谁：master
        self.master = master
        
        self.create()

    def destroy(self):
        super(ShowImageFrame,self).destroy()
    
    def create(self):
        # 1、添加滚动条
        self.picCanvasHorScrollbar = \
            tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.picCanvasVerScrollbar = \
            tk.Scrollbar(self, orient=tk.VERTICAL)        
            
        # 2、添加一个图片显示画布
        self.picCanvas = tk.Canvas(self, \
                            scrollregion=(0, 0, 1000, 1000), \
                            yscrollcommand=self.picCanvasVerScrollbar.set, \
                            xscrollcommand=self.picCanvasHorScrollbar.set )
        # 3、在移动滚动条时，调用画布组件的相应函数        
        self.picCanvasHorScrollbar['command'] =  self.picCanvas.xview                  
        self.picCanvasVerScrollbar['command'] =  self.picCanvas.yview 
        
        # Bottom-right corner resize widget
        # 右下角上的一个像三角形的三条斜线组件，
        # 可以拖动改变画布大小，不过如果这个Frame是在别的
        # 容器中，拖动他不起作用。
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(column=1, row=1, sticky=(tk.S,tk.E))
        
        # 4、通过grid布局方式，设置三个组件的位置
        self.picCanvas.grid(column=0, row=0, sticky='NWES')
        self.picCanvasHorScrollbar.grid(column=0, row=1, sticky=(tk.W,tk.E))
        self.picCanvasVerScrollbar.grid(column=1, row=0, sticky=(tk.N,tk.S))
        
        # 5、设置这个Frame在改变大小时，只对画布有效果。
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 6、设置我自己这个Frame在父容器的位置
        # Todo:这是不是应该在父容器里面调用这句话？
        # 因为只有父容器才知道把他安排到哪里。
        #self.grid(row=0,column=0,sticky='NSEW')  


# 继承父类
class MyShowOneImageFrame(ShowImageFrame):
    def __init__(self,master):
        super(MyShowOneImageFrame,self).__init__(master)
        
        self.imageFlag = 0 # 用来表示当期那是否有展示图片
        self.picCanvasImage = None # 当前展示的图片的PhotoImage对象

        
        ###########################################################
        # 下面是用来测试显示图片的部分
        ###########################################################
        #filePath = "C:\\Users\\Administrator\\Desktop\\图片\\公众号资源\\3.png"
        #image = Image.open(filePath)
        #self.showImage(image)

    def destroy(self):
        super(MyShowOneImageFrame,self).destroy()
        
    def setGrid(self,x,y):
        #tk.Grid.rowconfigure(self.master,0,weight=1)    
        #tk.Grid.columnconfigure(self.master,0,weight=1)
        
        self.grid(row=x,column=y,sticky='NSEW')  
        
    def showImage(self,image):
        '''
            传入image对象， 在画布的右上角进行显示。
        '''
        self.image = image
        # 获取图像大小，为了和Canvas的坐标相对应
        (x,y) = image.size
        self.picCanvasImage = ImageTk.PhotoImage(image)
        
        # 设置滚动条的滚动范围，以便显示整个图片
        self.picCanvas['scrollregion'] = (0,0,x,y)
        
        # 这个create_image的前两个参数，图片的位置（position）：
        # 应该说的是将image图片的中心点，放在画布的什么位置
        self.picCanvas.create_image(x/2,y/2,image = self.picCanvasImage)
        
        # 设置图像已经显示的标志。
        self.imageFlag = 1

    def refresh(self):
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
    
    def clean(self):
        self.image = None
        self.picCanvas.delete(tk.ALL)
        self.imageFlag = 0



class MyInputStringFrame(tk.Frame):
    def __init__(self,master):
        super(MyInputStringFrame,self).__init__(master)
        # 记住父容器是谁：master
        self.master = master
        # 创建自己的组件
        self.create()


    def destroy(self):
        super(MyInputStringFrame,self).destroy()

    def create(self):
        # 这些组件的容器就是这个类本身：
        # 0、声明一个字体类型，添加一个Label        
        self.showFont = tkFont.Font(family='微软雅黑',size = '16')
        
        self.inputStringLabel = tk.Label(self,text="二维码内容",wraplength=1,font = self.showFont) # 父容器就是self，这个frame
        # 这里还有个知识点：wraplength，让他换行。参考：
        # https://stackoverflow.com/questions/17650232/python-tkinter-label-orientation
        self.inputStringLabel.grid(row = 0,column = 0,sticky='NW') # 放在父容器的第1行第1列。
        # 1、添加一个输入文本框和对应的垂直滚动条
        # 垂直滚动条
        self.txtVerScrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        
        # 实例化一个文本显示区域
        self.txtArea = tk.Text(self,  width = 48,\
                            yscrollcommand=self.txtVerScrollbar.set )
        
        self.txtVerScrollbar['command'] = self.txtArea.yview
        
        self.txtArea.grid(row=0,column=1,columnspan=4,sticky='NEWS')# 第1行，第2列，跨越4列
        self.txtVerScrollbar.grid(row = 0,column=5,sticky='NS') # 第1行，第6列
        
        # 2、添加一个按键，用来触发事件输入事件
        self.createButton = tk.Button(self,width = 9,relief = 'raised',\
                                         fg = 'brown', text = "生成二维码",\
                                         font = self.showFont,\
                                         command = self.createQRCode )
        self.createButton.grid(row = 1,column=4,columnspan=2,sticky='NSEW')
    
        # 在create里面，安排当我自己这个Frame变大的时候，
        # 哪一行哪一列跟着变化。
        tk.Grid.rowconfigure(self,0,weight=1)    
        tk.Grid.columnconfigure(self,1,weight=1)  
        
        
    def setGrid(self,x,y):
        tk.Grid.rowconfigure(self.master,x,weight=1)    
        tk.Grid.columnconfigure(self.master,y,weight=1)    
        self.grid(row = x,column=y,sticky='NSEW')
        
    
    def createQRCode(self):
        data = self.txtArea.get(0.0,tk.END)
        
        # 这里应该直接调用父类中的创建二维码的函数
        self.master.subFrameCallHandler('NEW_QRCODE',data)

    

if __name__== "__main__":
    root = tk.Tk()
    app = MyInputStringFrame(master = root)
    app.setGrid(0,0)
    app.mainloop()
    