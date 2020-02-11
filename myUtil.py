import tkinter as tk
import tkinter.font as tkFont
from PIL import Image

# 参考 http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
# 参考 https://www.cnblogs.com/hhh5460/p/6664021.html?utm_source=itdadao&utm_medium=referral
class SimpleDialog():
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        
        self.top.title("参数输入")        
        #self.top.geometry('300x200')
        self.top.resizable(width=False,height=False)
        
        self.input = {}
        self.input['row'] = 0
        self.input['column'] = 0        
        self.create()
    
    def getInput(self):
        return (self.input['row'],self.input['column'])
    
    
    def create(self):        
        self.inputFont = tkFont.Font(family='微软雅黑',size = '16')
        self.inputFont2 = tkFont.Font(family='微软雅黑',size = '12')
        
        self.label = tk.Label(self.top,text = "输入分成的行列数",font = self.inputFont)
        self.labelRow = tk.Label(self.top,text = "行数",font = self.inputFont)
        self.labelColumn = tk.Label(self.top,text = "列数",font = self.inputFont)
        self.entryRow = tk.Entry(self.top,font = self.inputFont)
        
        self.entryColumn = tk.Entry(self.top,font = self.inputFont)
        self.buttonOk = tk.Button(self.top,text=' OK ',command = self.inputOK,font = self.inputFont2)
        self.buttonCancle = tk.Button(self.top,text='Cancle',command = self.inputCancle,font = self.inputFont2)
        
        self.label.grid( row=0,column=0,columnspan=4 )        
        self.labelRow.grid( row=1,column=0,columnspan=2  )  
        self.entryRow.grid( row=1,column=2,columnspan=2  )        
        self.labelColumn.grid( row=2,column=0,columnspan=2  )
        self.entryColumn.grid( row=2,column=2,columnspan=2  )
        
        self.buttonCancle.grid( row=3,column=2 ,sticky = 'NWS')
        self.buttonOk.grid( row=3,column=3 ,sticky = 'NES')
        
    def inputOK(self):
        self.input['row'],self.input['column']=(self.entryRow.get(),self.entryColumn.get())
        self.top.destroy()
    
    def inputCancle(self):
        self.input['row'],self.input['column']=(0,0)
        self.top.destroy()

# 参考：https://www.cnblogs.com/xiaohai2003ly/p/8778618.html
class ImageDivider():
    def __init__(self):
        pass
    
    def addMargin(self,image):
        localImage = Image.new('RGB',image.size,(255,255,255))
        MARGIN = 16
        
        newWidth = image.size[0]+2*MARGIN 
        newHeight = image.size[1]+2*MARGIN
        localImage = Image.new('RGB',(newWidth,newHeight),(255,255,255))
        localImage.paste(image,(MARGIN,MARGIN,newWidth-MARGIN,newHeight-MARGIN))
        return localImage
    
    def divide(self,image,rowNumber,columnNumber):        
        row = rowNumber
        column = columnNumber
        
        # Padding 表示用2像素单位对图像进行分格。
        PADDING = 8

        # row，表示要将图片分成多少行，值不能小于1，不能大于图像的纵向像素数
        row = int(row) if row>1 else 1
        row = row if row<image.size[1] else image.size[1]
        # column，图片分成多少列。
        column = int(column) if column > 1 else 1
        column = column if column < image.size[0] else image.size[0]
        
        # 如果1行1列，直接给图像价格边框，返回新的图像。
        if column*row == 1:
            return self.addMargin(image)
        
        # 计算新图像的宽和高
        newX = image.size[0]+(column-1)*PADDING
        newY = image.size[1]+(row-1)*PADDING

        # 计算给一个小格子图像的宽和高
        Xunit = int(round(image.size[0]/column))
        Yunit = int(round(image.size[1]/row))       
        
        # 新建一张白纸，用来粘贴小格子图像
        newImage = Image.new('RGB',(newX,newY),(255,255,255))
        
        for i in range(row):
            for j in range(column):        
                # 将一张图划分成row行，column列，
                # 计算第i+1行，第j+1列小格子的左上角、右下角坐标
                tempX1 = (j)*Xunit if image.size[0] > (j)*Xunit else image.size[0]
                tempY1 = (i)*Yunit if image.size[1] > (i)*Yunit else image.size[1]
                tempX2 = (j+1)*Xunit if image.size[0] > (j+1)*Xunit else image.size[0]
                tempY2 = (i+1)*Yunit if image.size[1] > (i+1)*Yunit else image.size[1]
                
                box=(tempX1,tempY1,tempX2,tempY2)
                # 根据box确定的坐标，取出image对应区域的图像，生成一份临时图像。
                tempImage = image.crop(box)
                # 将临时图像贴到对应的白纸图像上，每贴一张，留下一些空白。
                newImage.paste(tempImage,(j*PADDING+box[0],i*PADDING+box[1],j*PADDING+box[2],i*PADDING+box[3]))
        # 给图像加个白边，返回新生成的图像
        return self.addMargin(newImage)