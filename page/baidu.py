#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：baidu.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:58
-------------------------------------

"""


from page.BasePage import BasePage
from utils.logging_util import log


class BaiduPage(BasePage):

    input = ("id", "kw")
    search_button = ("id", "su")

    def baidu_input(self, text):
        self.send_keys(self.input, text)
        log.info(f"百度输入：{text}")

    def click_search_button(self):
        self.click(self.search_button)
        log.info("点击百度搜索按钮")
