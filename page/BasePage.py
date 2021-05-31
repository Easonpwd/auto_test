#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

-------------------------------------
@Project ：auto_test
@File    ：BasePage.py
@IDE     ：PyCharm
@Author  ：coke
@Time    ：2021/05/31 17:32
-------------------------------------

"""
import datetime
import os
from time import sleep, strftime
import allure
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from utils.logging_util import Logger

log = Logger()

driver = None


class BasePage:
    """
    多个用例执行需先退出游览器，重新实例化游览器。
    如果不使driver为空就会接着使用上一个driver，
    但是因为游览器已经关闭driver就会报错，所以需
    要重新实例化一个driver。
    """

    def __init__(self):
        global driver
        if not driver:
            # 获取驱动
            ChromeDriverPath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                            "driver/chromedriver.exe")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("disable-infobars")  # 去掉Chrome提示受到自动软件控制
            chrome_options.add_argument("--window-size=1920,1080")  # 指定浏览器分辨率
            chrome_options.add_argument('start-fullscreen')  # 游览器全屏
            # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            # 是你想指定的下载路径
            out_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "live_download_file")
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            driver = webdriver.Chrome(executable_path=ChromeDriverPath, options=chrome_options)
            self.driver = driver
            self.timeout = 20  # 查找元素的超时时间
            self.wait = WebDriverWait(self.driver, self.timeout)
        else:
            self.driver = driver

    # 打开游览器
    def open_url(self, url):
        try:
            log.info(f'打开 {url} 网址进行测试')
            self.driver.get(url)

        except Exception as e:
            log.error(f'打开网址 --> 失败：{e}')
            assert False

    # 获取当前网址
    def get_current_url(self):
        sleep(1)
        url_result = self.driver.current_url
        log.info(f'获取当前页面的网址为：{url_result}')
        return url_result

    # 获取当前网页title
    def get_page_title(self):
        sleep(0.5)
        title_name = self.driver.title
        log.info(f'获取当前页面的名称为：{title_name}')

        return title_name

    # 最大化游览器
    def max_browser(self):
        try:
            self.driver.maximize_window()
            log.info("放大游览器")
        except Exception as e:
            log.error(f'放大游览器失败 --> 失败：{e}')
            assert False

    # 切换窗口
    def switch_to_page(self, select_window):
        """
        :param select_window: 选择的窗口具柄
        选择需要填第几个按照索引来选
        :return:
        """
        try:
            log.info("当前正在获取当前游览器所有窗口句柄")
            sleep(1)
            webs = self.driver.window_handles  # 获取当前游览器所有窗口句柄
            self.driver.switch_to.window(webs[select_window])
            log.info(f"已切换到您选择的第【{select_window + 1}】个页面")
            sleep(1)
        except Exception as e:
            log.info(f'切换网页失败：{e}')

    # 选择元素
    def find_element(self, t_selector):
        """
           定位元素
           :param t_selector: 元组 示例：('css','id')
           :return ele: 元素
        """
        global locator_type
        try:
            selector = t_selector[0]
            value = t_selector[1]
            if selector.upper() == 'ID':
                locator_type = By.ID
            elif selector.upper() == 'NAME':
                locator_type = By.NAME
            elif selector.upper() == 'CLASS':
                locator_type = By.CLASS_NAME
            elif selector.upper() == 'TAG':
                locator_type = By.TAG_NAME
            elif selector.upper() == 'CSS':
                locator_type = By.CSS_SELECTOR
            elif selector.upper() == 'XPATH':
                locator_type = By.XPATH
            elif selector.upper() == 'LINK_TEXT':
                locator_type = By.LINK_TEXT
            elif selector.upper() == 'PARTIAL_LINK_TEXT':
                locator_type = By.PARTIAL_LINK_TEXT
            ele = WebDriverWait(self.driver, 10, 0.3).until(ec.visibility_of_element_located((locator_type, value)))
            return ele
        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            log.error(f"{t_selector}元素不能识别，原因是{e.__str__()}")
            self.screenshot("元素识别失败")

            assert False


    # 文本框输入
    def send_keys(self, selector, text):
        ele = self.find_element(selector)
        try:
            ele.send_keys(text)
            # log.info(f"在元素 [{selector[0], selector[1]}]-->输入{text}")

        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            self.screenshot("文本框输入异常")
            log.error(f'在元素 {selector} 输入内容 --> 失败：{e}')

            assert False

    # 元素清空输入框
    def clear(self, selector):
        ele = self.find_element(selector)
        try:
            ele.clear()
            log.info("清空输入框")
        except Exception as e:
            self.screenshot("清空文本框异常")

            log.error(e)

    # 清空输入
    def clear_and_input(self, selector, text):

        try:
            self.clear(selector)
            self.sendkeys(selector, text)
            log.info(f"输入：{text}")
        except Exception as e:
            self.screenshot("清空再输入异常")
            log.error(e)

    # 模拟键盘清空输入框
    def clear_textarea(self, selector, text):
        """清空文本框"""
        ele = self.find_element(selector)
        try:
            action = ActionChains(self.driver)
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
            log.info("清空文本框")
            self.sendkeys(selector, text)
            return ele
        except Exception as e:
            self.screenshot("模拟键盘清空文本框异常")
            log.error(f"清空文本框 --> 失败：{e}")

            assert False

    def click(self, selector):  # 点击
        """点击元素"""
        ele = self.find_element(selector)
        try:
            ele.click()
            # log.info(f"点击元素 [{selector[0], selector[1]}]")
            return ele

        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            self.screenshot("点击异常")
            log.error(f"点击元素 --> 失败：{e}")

            assert False

    def click_css(self, selector, number: int):  # css点击
        """点击css元素"""
        ele = self.find_elements(selector)[number]
        try:
            ele.click()
            # log.info(f"点击元素 [{selector[0], selector[1]}]")
            return ele

        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            self.screenshot(f"点击----> {selector} 异常")
            log.error(f"点击元素 --> 失败：{e}")
            assert False

    def check_all(self, selector):  # 键盘全选
        ele = self.find_element(selector)
        try:
            ele.send_keys(Keys.CONTROL, "a")
            log.info(f"ent Element {selector[0], selector[1]}")
        except Exception as e:
            self.screenshot(f"键盘模拟全选----> {selector} 异常")
            log.error(e)

            assert False

    def ent(self, selector):  # 回车
        ele = self.find_element(selector)
        try:
            ele.send_keys(Keys.ENTER)
            log.info(f"ent Element {selector[0], selector[1]}")
        except Exception as e:
            self.screenshot(f"键盘模拟回车----> {selector} 异常")
            log.error(e)

            assert False

    def toast_assert(self, toast_name):  # 提示断言
        toast = ("xpath", f"//div[@role = 'alert']/p[contains(text(),'{toast_name}')]")
        ele = self.find_element(toast)
        try:
            # 判断元素是否显示
            ele.is_displayed()
            sleep(0.5)
            assert toast_name in self.ele_text(toast)
            log.info(f"toast校验成功，toast提示：【{toast_name}】")
        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            self.screenshot("断言toast异常")
            log.error(f"校验失败【{False}】{e}")

            assert False

    # 断言文本内容
    def text_assert(self, selector, text):
        sleep(1)
        texts = self.find_element(selector).text
        try:
            log.info(f"正在校验【{text}】文本是否存在于页面内")
            assert text in texts
            log.info(f"校验成功,【{text}】文本在页面内")
        except Exception as e:
            allure.dynamic.issue(url=self.driver.current_url, name=f"异常问题定位链接: {self.driver.current_url}")
            self.screenshot(f"校验【{text}】失败")
            log.error(f"{selector} {e}")

            assert False

    # 元素文本
    def ele_text(self, selector):
        """
        :param selector: 截图说明
        :return ele: 元素文本
        """
        ele = self.find_element(selector).text
        return ele

    # 关闭当前页面
    def close_page(self):
        self.driver.close()
        log.info("当前页面 --> 关闭")

    # 游览器关闭
    def quit_browser(self):
        self.driver.quit()
        log.info('浏览器 --> 退出')
        global driver
        driver = None

    # 游览器返回上一步
    def back_browser(self):
        self.driver.back()
        log.info('浏览器 --> 返回')

    # 游览器刷新
    def refresh_browser(self):
        self.driver.refresh()
        sleep(0.5)
        log.info('浏览器 --> 刷新')

    # 下拉选择
    def pull_down(self, selector, x):
        ele = self.find_element(selector)
        if type(x) is int:
            Select(ele).select_by_index(x)  # 根据下拉列表的索引选中
        else:
            Select(ele).select_by_visible_text(x)  # 根据下拉文本选中

        try:
            log.info(f"Click Element [{selector[0], selector[1]},{x}]")

        except NameError as e:
            log.error(e)

    # alert 弹窗确认
    def alert_accept(self):
        log.info("弹窗确定")
        self.driver.switch_to.alert.accept()

    # 截图
    def screenshot(self, name):
        """
        :param name: 截图说明
        :return:
        """
        # 通过全局变量获取文件夹路径
        sleep(1)
        new_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "screenshot")
        img_name = f"{name}_{strftime('%Y-%m-%d %H-%M-%S')}.png"
        # 判断文件夹是否存在，不存在则创建
        is_dir = os.path.isdir(new_dir)
        if not is_dir:
            os.makedirs(new_dir)
        screenshot_paths = os.path.join(new_dir, img_name)
        self.driver.get_screenshot_as_file(screenshot_paths)
        with open(screenshot_paths, "rb", ) as f:
            img = f.read()
            allure.attach(img, name, allure.attachment_type.PNG)
        log.info(f" {img_name} 已截图")

    # 鼠标 悬停
    def mouse_hover(self, selector):
        ele = self.find_element(selector)

        try:
            log.info(f"鼠标悬停在 Element {selector[0], selector[1]}")
            ActionChains(self.driver).move_to_element(ele).perform()

        except NameError as e:
            self.screenshot("鼠标悬停异常")
            log.error(e)

    # 获取源码
    def get_page_source(self):
        yuanma = self.driver.page_source
        return yuanma

    # 执行js命令
    def execute_script(self, js):
        """
        :param js: js指令
        :return:
        """
        try:
            self.driver.execute_script(js)
        except Exception as e:
            log.error(e)