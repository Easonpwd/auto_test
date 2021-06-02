#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：run_all.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:40
-------------------------------------

"""
import os
import pytest
from utils.allure_environment_util import environment

allure_path = os.path.join(os.path.join(os.path.dirname(os.getcwd()), "allure-results"))
pytest.main(["-v", "-s", "-n", "auto", "../testcase"])
environment()
os.system(f"allure generate {allure_path} -o ../allure-results/report --clean")
