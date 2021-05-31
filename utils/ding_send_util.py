#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：ding_send_util.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:23
-------------------------------------

"""

import os
import jenkins
import json
import urllib3
import os
from utils.yaml_util import YamlUtil

jenkins_login = YamlUtil('jenkins.yaml').read_data['login']
# jenkins登录地址
jenkins_url = "xxxxx"
# 获取jenkins对象
server = jenkins.Jenkins(jenkins_url, username=jenkins_login['user'], password=jenkins_login['password'])
# job名称
job_name = "job/auto_test/"
# job的url地址
job_url = jenkins_url + job_name
# 获取最后一次构建
job_last_build_url = server.get_info(job_name)['lastBuild']['url']
# 报告地址
report_url = job_last_build_url + 'allure'


'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''


def DingTalkSend():
    d = {}
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打开prometheusData 获取需要发送的信息
    f = open(path + r'/allure-report/export/prometheusData.txt', 'r')
    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    print(d)
    f.close()
    retries_run = d.get('launch_retries_run')  # 运行总数
    print('运行总数:{}'.format(retries_run))
    status_passed = d.get('launch_status_passed')  # 通过数量
    print('通过数量：{}'.format(status_passed))
    status_failed = d.get('launch_status_failed')  # 不通过数量
    print('通过数量：{}'.format(status_failed))
    status_broken = d.get('launch_status_broken')  # 异常数量
    print('通过数量：{}'.format(status_broken))

    # 钉钉推送

    url = 'xxxxxxx'  # webhook
    con = {"msgtype": "text",
           "text": {
               "content": "xxxxx"
                          f"测试环境：{os.getenv('TEST')}环境"
                          "\n测试用例概述:"
                          "\n基本功能：登陆，创建直播"
                          "\n设置模块：基本信息，通知中心，分发平台，操作日志"
                          "\n资源中心：资源包购买【短信除外】，账户升级"
                          "\n运行总数:" + retries_run +
                          "\n通过数量:" + status_passed +
                          "\n失败数量:" + status_failed +
                          "\n异常数量:" + status_broken +
                          "\n构建地址：\n" + job_url +
                          "\n报告地址：\n" + report_url
           }
           }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(con)
    jd = bytes(jd, 'utf-8')
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    DingTalkSend()


