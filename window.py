import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import threshold
import cv2
import numpy as np
import os

color_gray = "#BFB9B9"
#窗口大小‘1000 * 600’

class mainwindow(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        self.src_path = ''
        self.cur_mode = 'RGB阈值调节'
        self.img_origne, self.img_after = None, None   #原始图片以及处理后的图片
        self.imgbuf_origne, self.imgbuf_after = None, None     #原始展示图片以及处理后的展示图片(变形)
    #窗口本体初始化设置
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.minsize(width = 800, height = 600)
        self.geometry('1000x600')
        self.resizable(False, False)

    #窗口组件初始化设置
        #标签设置
        self.label_info = ttk.Label(self, text = 'img_size:')
        self.label_info.place(x = 15, y = 1)
        self.label_size = ttk.Label(self, text = 'no_image')
        self.label_size.place(x = 70, y = 1)
         
        self.label_img1 = ttk.Label(self, background = color_gray)
        self.label_img1.place(x = 15, y = 25, width = 480, height = 360)
        self.label_img2 = ttk.Label(self, background = color_gray)
        self.label_img2.place(x = 505, y = 25, width = 480, height = 360)
        #图片文件选择，保存
        self.select_button = ttk.Button(self, text = '选择图片', width = 20, command = self.select_img)
        self.select_button.place(x = 200, y = 400)

        self.save_button = ttk.Button(self, text = '保存', width = 20, command = self.save_img)
        self.save_button.place(x = 380, y = 400)
        #复位按钮
        self.reset_button = ttk.Button(self, text = '重置滑块', width = 20, command = self.value_reset)
        self.reset_button.place(x = 560, y = 400)
        #设置模式转换下拉框
        self.options = ['RGB阈值调节', 'HSV阈值调节', 'LAB阈值调节', '灰度图像转换', '灰度阈值调节']
        self.combox = ttk.Combobox(self, values = self.options, width = 20, state = 'readonly')
        self.combox.current(0)
        self.combox.place(x = 15, y = 400, height = 25)
        self.combox.bind('<<ComboboxSelected>>', lambda event: self.mode_change())
        #图片选择对话框
        
        self.Gray_tr = threshold.Gray_translate(self, callback = self.update_img)
        self.Gray_mode = threshold.Gray_threshold(self, callback = self.update_img)
        self.LAB_mode = threshold.LAB_threshold(self, callback = self.update_img)
        self.HSV_mode = threshold.HSV_threshold(self, callback = self.update_img)
        self.RGB_mode = threshold.RGB_threshold(self, callback = self.update_img)
        self.Gray_tr.place(x = 15, y = 430)
        self.Gray_mode.place(x = 15, y = 430)
        self.HSV_mode.place(x = 15, y = 430)
        self.LAB_mode.place(x = 15, y = 430)
        self.RGB_mode.place(x = 15, y = 430)

    def select_img(self):
        path = filedialog.askopenfilename(
            parent = self, 
            title = '选择图片', 
            filetypes = [('所有图片', '*.jpg *.jpeg *.png'), ('jpg图片', '*.jpg *.jpeg'), ('png图片', '*.png')]
        )
        if path != '':
            self.src_path = path
            img = Image.open(path)      #RGB格式打开
            width = img.width
            height = img.height
            self.img_origne = img
            img = img.resize((480, 360), Image.Resampling.LANCZOS)
            self.imgbuf_origne = ImageTk.PhotoImage(img)
            self.label_img1.config(image = self.imgbuf_origne)
            self.label_size.config(text = '{:d}x{:d}'.format(width, height))
            
            self.Gray_tr.update_src(self.src_path)
            self.Gray_mode.update_src(self.src_path)
            self.RGB_mode.update_src(self.src_path) 
            self.LAB_mode.update_src(self.src_path)
            self.HSV_mode.update_src(self.src_path)
            self.Gray_tr.set_update()
            self.Gray_mode.set_threshold(0, '')
            self.LAB_mode.set_threshold(0, '')
            self.HSV_mode.set_threshold(0, '')
            self.RGB_mode.set_threshold(0, '')


    def save_img(self):
        path = filedialog.asksaveasfilename(
                parent = self, 
                title = '保存图片至',
                defaultextension = '.png',
                filetypes = [('所有图片', '*.jpg *.jpeg *.png'), ('jpg图片', '*.jpg *.jpeg'), ('png图片', '*.png')]
            )
        cv_img = np.array(self.img_after)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        
        if path != '' and self.img_after:
            cv2.imshow('CV预览', cv_img)
            cv2.waitKey()
            img = np.array(self.img_after)
            cv2.imwrite(path, img)
            print(path)

    def update_img(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        self.img_after = img_pil
        img_buff = img_pil.resize((480, 360), Image.Resampling.LANCZOS)
        self.imgbuf_after = ImageTk.PhotoImage(img_buff)
        self.label_img2.config(image = self.imgbuf_after)
        
    def __mode_clear(self):
        self.Gray_tr.place_forget()
        self.Gray_mode.place_forget()
        self.RGB_mode.place_forget()
        self.HSV_mode.place_forget()
        self.LAB_mode.place_forget()

    def mode_change(self):
        self.cur_mode = self.combox.get()
        match self.cur_mode:
            case 'RGB阈值调节':
                self.__mode_clear()
                self.RGB_mode.place(x = 15, y = 430)
                self.RGB_mode.set_threshold(0, '')
            case 'HSV阈值调节':
                self.__mode_clear()
                self.HSV_mode.place(x = 15, y = 430)
                self.HSV_mode.set_threshold(0, '')
            case 'LAB阈值调节':
                self.__mode_clear()
                self.LAB_mode.place(x = 15, y = 430)
                self.LAB_mode.set_threshold(0, '')
            case '灰度阈值调节':
                self.__mode_clear()
                self.Gray_mode.place(x = 15, y = 430)
                self.Gray_mode.set_threshold(0, '')
            case '灰度图像转换':
                self.__mode_clear()
                self.Gray_tr.place(x = 15, y = 430)
                self.Gray_tr.set_update()
            case _:
                pass

    def value_reset(self):
        match self.cur_mode:
            case 'RGB阈值调节':
                self.RGB_mode.reset()
            case 'HSV阈值调节':
                self.HSV_mode.reset()
            case 'LAB阈值调节':
                self.LAB_mode.reset()
            case '灰度阈值调节':
                self.Gray_mode.reset()
            case _:
                pass

    def set_ico(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(dir, 'img\\tubiao.ico')
        self.iconbitmap(img_dir)
