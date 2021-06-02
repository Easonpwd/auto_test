#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：conftest.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:34
-------------------------------------

"""

from page.baidu import BaiduPage
import pytest
from time import sleep
from utils.yaml_util import YamlUtil
import platform
import os

# logins = YamlUtil("login.yaml").read_data["login"]
# if platform.system().lower() == 'linux':
#     test = os.getenv('TEST')
#     env = logins[test]
# else:
#     env = logins["test3"]


@pytest.fixture
def open_baidu():
    """登录"""
    BaiduPage().open_url(YamlUtil.get_config()["baidu"]["url"])
    sleep(1)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")