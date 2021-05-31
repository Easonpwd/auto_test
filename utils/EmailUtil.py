#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：EmailUtil.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/01/08 10:34
-------------------------------------

"""

import smtplib, os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from utils.yaml_util import YamlUtil


class EmailUtil:

    def __init__(self):
        self.cr = YamlUtil.get_config()["email"]
        self.host = self.cr['server_host']
        self.port = int(self.cr['server_port'])
        self.user = self.cr['user']
        self.password = self.cr['password']
        # self.smtp = smtplib.SMTP('smtp.qq.com') # 不加密
        self.smtp = smtplib.SMTP_SSL(self.host, self.port)  # SSL加密
        self.smtp.login(self.user, self.password)
        self.sender = self.user
        self.to_addrs = self.cr['to_addrs'].replace('[', '').replace(']', '').replace('\'', '').replace(', ', ',').split(',')

    def send(self, title, body, file, to_addrs=None):

        message = MIMEMultipart() # 带附件的邮件
        message.attach(MIMEText(body))

        file_name = os.path.basename(file)
        fp = open(file, mode='rb')
        att = MIMEImage(fp.read()) # 图片附件
        fp.close()
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f'attachment; filename={file_name}'
        message.attach(att)

        message['subject'] = Header(title, 'utf-8')
        message['From'] = Header(self.sender, 'utf-8')
        message['To'] = Header(str(to_addrs), 'utf-8')
        if to_addrs:
            self.to_addrs = to_addrs
        self.smtp.sendmail(self.sender, self.to_addrs, message.as_string())

        self.close()

    def send_all(self, title, body, files, to_addrs=None):

        textApart = MIMEText(body)
        htmlFile = files
        htmlApart = MIMEApplication(open(htmlFile, 'rb').read())
        htmlApart.add_header('Content-Disposition', 'attachment', filename=htmlFile)
        m = MIMEMultipart()
        m.attach(textApart)
        m.attach(htmlApart)
        m['Subject'] = title
        m['From'] = self.sender
        if to_addrs:
            self.to_addrs = to_addrs
        self.smtp.sendmail(self.sender, self.to_addrs, m.as_string())

        self.close()

    def close(self):
        self.smtp.close()


if __name__ == "__main__":
    pass

