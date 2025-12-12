import tkinter as tk
from tkinter import ttk
import mixslider
from PIL import Image
import numpy as np
import cv2

color_gray = "#BFB9B9"

class Gray_translate(ttk.Frame):
    def __init__(self, master = None, callback = None):
        super().__init__(master)
    #自带属性
        self.src_path = None
        self.callback = callback
    #界面设置
        self.config(width = 950, height = 160)
        self.label = ttk.Label(self, text = '说明：该工具采用的彩色图像->灰度图像转换方法使用的是加权平均法', font = 10)
        self.label2 = ttk.Label(self, text = '该功能主要用于灰度图像转换，使用灰度阈值调节也能对彩色图像进行阈值调节', font = 10)
        self.label.place(x = 1, y = 1)
        self.label2.place(x = 1, y = 31)

    def set_update(self):
        self.callback_handler()

    def callback_handler(self):
        if self.src_path:
            img = Image.open(self.src_path)
            img_cv2 = np.array(img)
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2GRAY)
            self.callback(img_cv2)

    def update_src(self, path):
        self.src_path = path

class Gray_threshold(ttk.Frame):
    def __init__(self, master = None, callback = None):
        super().__init__(master)
    #自带属性
        self.src_path = None
        self.callback = callback
        self.threshold = {
            'Gray_l' : 0, 'Gray_h' : 255,
        }
    #界面设置
        self.config(width = 950, height = 160)
        self.slider1 = mixslider.slider(self, 0, 255, 0, 'G_l', self.set_threshold)
        self.slider2 = mixslider.slider(self, 0, 255, 255, 'G_h', self.set_threshold)
        self.slider1.place(x = 1, y = 1)
        self.slider2.place(x = 1, y = 26)

    def reset(self):
        self.slider1.value_reset(0)
        self.slider2.value_reset(1)

    def set_threshold(self, value, text):
        match text:
            case 'G_l':
                self.threshold['Gray_l'] = value
            case 'G_h':
                self.threshold['Gray_h'] = value
            case _:
                pass
        self.callback_handler()

    def callback_handler(self):
        if self.src_path:
            img = Image.open(self.src_path)
            img_cv2 = np.array(img)
            img_mode = img.mode
            if img_mode == 'RGB':
                img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2GRAY)
            low = self.threshold['Gray_l']
            high = self.threshold['Gray_h']
            mask_cv2 = cv2.inRange(img_cv2, low, high)

            self.callback(mask_cv2)

    def update_src(self, path):
        self.src_path = path


class RGB_threshold(ttk.Frame):
    def __init__(self, master = None, callback = None):
        super().__init__(master)
    #属性设置
        self.src_path = None
        self.callback = callback
        self.threshold = {
            'R_l': 0, 'R_h': 255,
            'G_l': 0, 'G_h': 255,
            'B_l': 0, 'B_h': 255,
        }
        self.low = np.array([self.threshold['B_l'], self.threshold['G_l'], self.threshold['R_l']])
        self.high = np.array([self.threshold['B_h'], self.threshold['G_h'], self.threshold['R_h']])
    #界面设置
        self.config(width = 950, height = 160)
        self.frame_style = ttk.Style()
        self.frame_style.configure('TFrame')

        self.slider1 = mixslider.slider(self, 0, 255, 0, 'R_l', self.set_threshold)
        self.slider2 = mixslider.slider(self, 0, 255, 255, 'R_h', self.set_threshold)
        self.slider3 = mixslider.slider(self, 0, 255, 0, 'G_l', self.set_threshold)
        self.slider4 = mixslider.slider(self, 0, 255, 255, 'G_h', self.set_threshold)
        self.slider5 = mixslider.slider(self, 0, 255, 0, 'B_l', self.set_threshold)
        self.slider6 = mixslider.slider(self, 0, 255, 255, 'B_h', self.set_threshold)
        self.slider1.place(x = 1, y = 1)
        self.slider2.place(x = 1, y = 26)
        self.slider3.place(x = 1, y = 51)
        self.slider4.place(x = 1, y = 76)
        self.slider5.place(x = 1, y = 101)
        self.slider6.place(x = 1, y = 126)

    def reset(self):
        self.slider1.value_reset(0)
        self.slider2.value_reset(1)
        self.slider3.value_reset(0)
        self.slider4.value_reset(1)
        self.slider5.value_reset(0)
        self.slider6.value_reset(1)

    def set_threshold(self, value, text):
        match text:
            case 'R_l':
                self.threshold['R_l'] = value
            case 'R_h':
                self.threshold['R_h'] = value
            case 'G_l':
                self.threshold['G_l'] = value
            case 'G_h':
                self.threshold['G_h'] = value
            case 'B_l':
                self.threshold['B_l'] = value
            case 'B_h':
                self.threshold['B_h'] = value
            case _:
                pass
        self.callback_handler()
    
    def callback_handler(self):
        if self.src_path:
            img = Image.open(self.src_path)
            img_cv2 = np.array(img)
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2BGR)
            low = np.array([self.threshold['B_l'], self.threshold['G_l'], self.threshold['R_l']])
            high = np.array([self.threshold['B_h'], self.threshold['G_h'], self.threshold['R_h']])
            mask_cv2 = cv2.inRange(img_cv2, low, high)
            self.callback(mask_cv2)
        
    def update_src(self, path):
        self.src_path = path


class HSV_threshold(ttk.Frame):
    def __init__(self, master = None, callback = None):
        super().__init__(master)
    #属性设置
        self.src_path = None
        self.callback = callback
        self.threshold = {
            'H_l': 0, 'H_h': 255,
            'S_l': 0, 'S_h': 255,
            'V_l': 0, 'V_h': 255,
        }
    #界面设置
        self.config(width = 950, height = 160)
        self.frame_style = ttk.Style()
        self.frame_style.configure('TFrame')

        self.slider1 = mixslider.slider(self, 0, 179, 0, 'H_l', self.set_threshold)
        self.slider2 = mixslider.slider(self, 0, 179, 179, 'H_h', self.set_threshold)
        self.slider3 = mixslider.slider(self, 0, 255, 0, 'S_l', self.set_threshold)
        self.slider4 = mixslider.slider(self, 0, 255, 255, 'S_h', self.set_threshold)
        self.slider5 = mixslider.slider(self, 0, 255, 0, 'V_l', self.set_threshold)
        self.slider6 = mixslider.slider(self, 0, 255, 255, 'V_h', self.set_threshold)
        self.slider1.place(x = 1, y = 1)
        self.slider2.place(x = 1, y = 26)
        self.slider3.place(x = 1, y = 51)
        self.slider4.place(x = 1, y = 76)
        self.slider5.place(x = 1, y = 101)
        self.slider6.place(x = 1, y = 126)

    def reset(self):
        self.slider1.value_reset(0)
        self.slider2.value_reset(1)
        self.slider3.value_reset(0)
        self.slider4.value_reset(1)
        self.slider5.value_reset(0)
        self.slider6.value_reset(1)
    
    def set_threshold(self, value, text):
        match text:
            case 'H_l':
                self.threshold['H_l'] = value
            case 'H_h':
                self.threshold['H_h'] = value
            case 'S_l':
                self.threshold['S_l'] = value
            case 'S_h':
                self.threshold['S_h'] = value
            case 'V_l':
                self.threshold['V_l'] = value
            case 'V_h':
                self.threshold['V_h'] = value
            case _:
                pass
        self.callback_handler()

    def callback_handler(self):
        if self.src_path:
            img = Image.open(self.src_path)
            img_cv2 = np.array(img)
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2HSV)
            low = np.array([self.threshold['H_l'], self.threshold['S_l'], self.threshold['V_l']])
            high = np.array([self.threshold['H_h'], self.threshold['S_h'], self.threshold['V_h']])
            mask_cv2 = cv2.inRange(img_cv2, low, high)
            self.callback(mask_cv2)

    def update_src(self, path):
        self.src_path = path


class LAB_threshold(ttk.Frame):
    def __init__(self, master = None, callback = None):
        super().__init__(master)
    #属性设置
        self.src_path = None
        self.callback = callback
        self.threshold = {
            'L_l': 0, 'L_h': 255,
            'A_l': 0, 'A_h': 255,
            'B_l': 0, 'B_h': 255,
        }
    #界面设置
        self.config(width = 950, height = 160)
        self.frame_style = ttk.Style()
        self.frame_style.configure('TFrame')

        self.slider1 = mixslider.slider(self, 0, 255, 0, 'L_l', self.set_threshold)
        self.slider2 = mixslider.slider(self, 0, 255, 255, 'L_h', self.set_threshold)
        self.slider3 = mixslider.slider(self, 0, 255, 0, 'A_l', self.set_threshold)
        self.slider4 = mixslider.slider(self, 0, 255, 255, 'A_h', self.set_threshold)
        self.slider5 = mixslider.slider(self, 0, 255, 0, 'B_l', self.set_threshold)
        self.slider6 = mixslider.slider(self, 0, 255, 255, 'B_h', self.set_threshold)
        self.slider1.place(x = 1, y = 1)
        self.slider2.place(x = 1, y = 26)
        self.slider3.place(x = 1, y = 51)
        self.slider4.place(x = 1, y = 76)
        self.slider5.place(x = 1, y = 101)
        self.slider6.place(x = 1, y = 126)

    def reset(self):
        self.slider1.value_reset(0)
        self.slider2.value_reset(1)
        self.slider3.value_reset(0)
        self.slider4.value_reset(1)
        self.slider5.value_reset(0)
        self.slider6.value_reset(1)

    def set_threshold(self, value, text):
        match text:
            case 'L_l':
                self.threshold['L_l'] = value
            case 'L_h':
                self.threshold['L_h'] = value
            case 'A_l':
                self.threshold['A_l'] = value
            case 'A_h':
                self.threshold['A_h'] = value
            case 'B_l':
                self.threshold['B_l'] = value
            case 'B_h':
                self.threshold['B_h'] = value
            case _:
                pass
        self.callback_handler()

    def callback_handler(self):
        if self.src_path:
            img = Image.open(self.src_path)
            img_cv2 = np.array(img)
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2LAB)
            low = np.array([self.threshold['L_l'], self.threshold['A_l'], self.threshold['B_l']])
            high = np.array([self.threshold['L_h'], self.threshold['A_h'], self.threshold['B_h']])
            mask_cv2 = cv2.inRange(img_cv2, low, high)
            self.callback(mask_cv2)

    def update_src(self, path):
        self.src_path = path
