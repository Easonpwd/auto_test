#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：mysql_util.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:32
-------------------------------------

"""

import pymysql
from utils.yaml_util import YamlUtil
# from utils.ConfigUtil import ConfigReader
from utils.logging_util import Logger


class MysqlUtil:

    def __init__(self):
        self.database = YamlUtil.get_config()['database']
        self.__db_host = self.database['host']  # 属性应私有
        self.__db_port = int(self.database['port'])  # 注意，端口是int类型，不能有引号，否则会报错
        self.__db_user = int(self.database['user'])
        self.__db_password = self.database['password']

    def connect_mysql(self, database):
        """
        初始化mysql的connect对象，连接数据库
        :param database: 要连接的数据库名字
        """
        try:
            # 通过配置文件获取数据库的host，port，user，password，charset
            self.database = YamlUtil.get_config()['database']
            self.__db = pymysql.connect(
                host=self.__db_host,
                port=self.__db_port,
                user=self.__db_user,
                password=self.__db_password,
                database=database,
                charset='utf8'
            )
        except Exception as e:
            Logger.error(f"无法登陆数据库，错误原因：{e}")

    def select(self, query):
        """
        运行mysql的select语句
        :param query: select语句
        :return: select_data：返回全部的select语句的数据
        """
        global cursor
        Logger.info(f"select语句为：{query}")
        try:
            # 定义游标，并通过execute执行sql语句
            cursor = self.__db.cursorsor()
            cursor.execute(query)
            # fetchall读取游标中的所有select数据
            select_data = cursor.fetchall()
            Logger.info("数据查询成功")
            # 返回select数据
            return select_data
        except Exception as e:
            Logger.error(f"select语句错误，错误原因是：{e}")
        finally:
            cursor.close()  # 关闭游标
            self.__db.close()  # 关闭数据库连接

    def insert(self, query):
        """
        运行mysql的select语句
        :param query: insert语句
        """
        global cursor
        Logger.info(f"insert语句为：{query}")
        try:
            # 定义游标，并通过execute执行insert语句
            cursor = self.__db.cursorsor()
            cursor.execute(query)
            # insert执行成功后commit提交数据
            cursor.execute("commit")
            Logger.info(f"数据插入成功")
        except Exception as e:
            Logger.error(f"insert 语句错误，原因是{e}")
            # insert失败后rollback回滚数据
            self.__db.rollback()
        finally:
            cursor.close()  # 关闭游标
            self.__db.close()  # 关闭数据库连接

    def delete(self, query):
        """
        运行mysql的delete语句
        :param query: delete语句
        """
        global cursor
        Logger.info(f"delete语句为：{query}")
        try:
            # 定义游标，并通过execute执行delete语句
            cursor = self.__db.cursorsor()
            cursor.execute(query)
            # delete执行成功后commit提交数据
            cursor.execute("commit")
            Logger.info("数据删除成功")
        except Exception as e:
            Logger.error(f"delete语句失败，原因：{e}")
            # delete失败后rollback回滚数据
            self.__db.rollback()
        finally:
            cursor.close()  # 关闭游标
            self.__db.close()  # 关闭数据库连接


if __name__ == "__main__":
    database = YamlUtil.get_config()['database']
    
    print(database['host'])
