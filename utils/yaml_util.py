#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：yaml_util.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:32
-------------------------------------

"""

import yaml
import os
from utils.logging_util import Logger

log = Logger()


class YamlUtil:

    """
    :param file_path: 输入data文件下的文件名称
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(YamlUtil, cls).__new__(cls)
        return cls.__instance

    # 获取yaml文件数据
    def __init__(self, file_path):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               f"../data/{file_path}")), encoding="UTF-8") as f:
            self.data = yaml.safe_load(f)

    # 返回 yaml文件数据
    @property
    def read_data(self):
        return self.data

    # 写入 yaml文件
    def write_yaml(self, path):
        with open(path, 'w+', encoding='utf-8') as f:
            yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True)

    @classmethod
    def get_config(cls):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               f"../config/config.yaml")), encoding="UTF-8") as f:
            return yaml.safe_load(f)


if __name__ == '__main__':
    pass