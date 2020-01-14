import tkinter as tk

from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create()
    
    def create(self):
        # 定义Master的标题栏
        self.master.title("GUI应用-Tk")
        # 替换应用的图标
        self.master.iconbitmap("sources/blackEight.ico")
        # 设置窗体最小大小，和最大大小：
        self.master.maxsize(1200,800)
        self.master.minsize(300,200)
        
        
        # 创建菜单栏
        
        # 创建显示文字的text widget 的Frame
        
        # 创建输入文字的Frame
        
#================================================
#==================== MAIN ======================
#================================================
if __name__=="__main__":
    root = tk.Tk()                 # 只能有一个tk.Tk()产生一个。
    app = Application(master=root)
    app.mainloop()