#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：file_util.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:32
-------------------------------------

"""
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import pyperclip
import platform
from time import sleep
import os
from utils.logging_util import log


# 文件上传
def uploading(file):
    uploading_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../data/img/{file}"))

    is_dir = os.path.exists(uploading_path)
    if is_dir:
        # 实例化键盘鼠标
        k = PyKeyboard()
        m = PyMouse()
        if platform.system().lower() == 'windows':
            log.info("您的系统是windows，正在使用windows系统的文件上传")
            log.info(f"您正在上传{file}文件")
            sleep(1)
            # 复制文件名称
            pyperclip.copy(uploading_path)
            sleep(1)
            # kb.tap_key(kb.shift_key) # 按下shift
            k.press_keys([k.control_key, 'v'])  # press_keys 输入多个键、组合键 粘贴文件名称
            k.tap_key(k.tab_key)  # tap_key 输入单个键
            k.tap_key(k.tab_key)  # tab
            k.tap_key(k.enter_key)  # 回车
            sleep(4)
            log.info(f"{file}文件上传完毕")
        elif platform.system().lower() == 'darwin':
            log.info("您的系统是darwin，正在使用mac系统的文件上传")
            # 实例化键盘和鼠标
            log.info(f"您正在上传{file}文件")
            # 呼出文件输入框
            k.press_keys(['Command', 'Shift', 'G'])
            # 获取屏幕大小
            x_dim, y_dim = m.screen_size()
            # 鼠标移入点击输入框，ui对象变更为系统文件上传输入框
            """
            m.click(x,y,button,n) 鼠标点击 
            x,y 是坐标位置 
            button 1表示左键，2表示点击右键 
            n 点击次数，默认是1次，2表示双击
            """
            m.click(x_dim // 2, y_dim // 2, 1)
            filepath = '/'
            # 复制文件路径开头的斜杠/
            pyperclip.copy(filepath)
            # 粘贴斜杠/
            k.press_keys(['Command', 'V'])
            sleep(0.5)
            # 输入文件的绝对路径
            k.type_string(uploading_path[1:]) if file.startswith("/") else k.type_string(file)
            # 操作键盘按回车键
            k.press_key('Return')
            sleep(1)
            k.press_key('Return')
            sleep(2)
            log.info(f"{file}文件上传完毕")
        elif platform.system().lower() == 'linux':
            log.info("您的系统是linux，正在使用linux系统的文件上传")
            # 实例化键盘和鼠标
            log.info(f"您正在上传{file}文件")
            sleep(3)
            # 输入文件的绝对路径
            k.type_string(uploading_path)
            # 操作键盘按回车键
            sleep(3)
            k.press_key('Return')
            sleep(3)
            log.info("正在回车")
            k.press_key('Return')
            sleep(3)
            log.info(f"{file}文件上传完毕")
    else:
        log.info("没有此文件，无法上传")


def file_download_exists(filepath):
    file = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "live_download_file")
    file_download = os.path.join(file, filepath)
    if os.path.exists(file_download):
        log.info("此文件存在")
    else:
        log.info("此文件不存在")
        assert False


if __name__ == '__main__':
    pass
