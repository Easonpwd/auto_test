#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：baidu_search_test.py
@IDE     ：PyCharm
@Author  ：chenff
@Time    ：2021/05/31 17:58
-------------------------------------

"""

from page.baidu import BaiduPage
import pytest
from utils.yaml_util import YamlUtil
from time import sleep


@pytest.mark.usefixtures("open_baidu")
class TestBaiduSearch:

    def setup(self):
        self.baidu = BaiduPage()

    @allure.feature("百度搜索功能")
    @allure.title("用例：搜索成功，搜索内容为：{text}")
    @pytest.mark.parametrize("text", YamlUtil("baidu_search.yaml").read_data["search"])
    def test_baidu_search(self, text):
        """
        测试百度搜索
        """
        self.baidu.baidu_input(text)
        sleep(2)
        self.baidu.click_search_button()
        sleep(2)

    def teardown(self):
        self.baidu.quit_browser()
