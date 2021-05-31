#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：allure_environment_util.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:23
-------------------------------------

"""

import shutil
import os


def environment():

    # allure测试报告环境配置路径
    allure_environment_path = (os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                            "allure-results"))
    # allure环境测试报告环境存放路径
    config_path = ((os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                 "config")))
    # allure环境
    shutil.copy(os.path.join(config_path, "environment.properties"), allure_environment_path)
    # allure 测试分类
    shutil.copy(os.path.join(config_path, "categories.json"), allure_environment_path)