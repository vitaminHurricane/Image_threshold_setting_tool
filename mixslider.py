import tkinter as tk
from tkinter import ttk

color_gray = "#BFB9B9"

class slider(ttk.Frame):
    def __init__(self, master = None, start = 0, end = 0, length = 0, text = '', callback = None):
        super().__init__(master)
        self.value ,self.start, self.end= start, start, end
        self.text = text
        self.callback = callback
    #划定组件区域大小
        self.config(width = 850 + 100, height = 25)
        self.slider_style = ttk.Style()
        self.slider_style.configure('TFrame')
    #滑块描述文本设置
        self.rolltext = ttk.Label(self, text = text)
        self.rolltext.place(x = 1, y = 2)
    #滑块设置
        self.rollbar = ttk.Scale(self, from_ = start, to = end, length = 850, value = length, command = lambda val:self.callback_handler())
        self.rollbar.place(x = 25, y = 1, height = 23)
        self.rollbar.bind('<B1-Motion>', lambda event:self.value_r2b())
        self.rollbar.bind('<ButtonRelease-1>', lambda event:self.value_r2b())
        self.rollbar.bind('<B2-Motion>', lambda event:self.value_r2b())
        self.rollbar.bind('<ButtonRelease-2>', lambda event:self.value_r2b())
        self.rollbar.bind('<B3-Motion>', lambda event:self.value_r2b())
        self.rollbar.bind('<ButtonRelease-3>', lambda event:self.value_r2b())
    #参数盒设置
        self.box = ttk.Spinbox(self, from_ = start, to = end, increment = 1, command = self.value_b2r)
        self.box.insert(0, length)
        self.box.place(x = 850 + 25, y = 2, width = 55, height = 23)
        self.box.bind('<Return>', lambda event:self.value_b2r())
    #转换与限幅函数
    def value_r2b(self):
        cur_value = int(self.rollbar.get())
        cur_value = self.__value_limit(cur_value)
        self.value = cur_value
        self.rollbar.config(value = self.value)
        self.box.delete(0, tk.END)
        self.box.insert(0, self.value)
        
    def value_b2r(self):
        if self.box.get() != '' or self.box.get().isdigit():
            cur_value = int(eval(self.box.get()))
            cur_value = self.__value_limit(cur_value)
            self.value = cur_value
        self.box.delete(0, tk.END)
        self.box.insert(0, self.value)
        self.rollbar.config(value = self.value)
        self.callback_handler()

    def __value_limit(self, value):
        if value > self.end:
            value = self.end
        elif value < self.start:
            value = self.start
        return value
    
    def value_reset(self, mode):
        if mode == 0:
            self.value = self.start
            self.box.delete(0, tk.END)
            self.box.insert(0, self.value)
            self.rollbar.config(value = self.value)
        else:
            self.value = self.end
            self.box.delete(0, tk.END)
            self.box.insert(0, self.value)
            self.rollbar.config(value = self.value)
        self.callback_handler()
    
    def callback_handler(self):
        self.callback(self.value, self.text)

        