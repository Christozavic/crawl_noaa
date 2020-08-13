# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import urllib3
import time

urllib3.disable_warnings()

__description__ = u'地震数据获取'
__author__ = 'kts'
__date__ = '2019-09-28'
__version__ = '1.0'

# 获取地址 https://www.avl.class.noaa.gov/saa/products/welcome
# 题目说明 通过解析上面的网址来进行数据订购，能够实现自动下单即可；选择（Infrared Atmospheric Sounding Interferometer 3X3 (IASI3X3)）
# 详细说明见 02_download_noaa说明文档.docx
# 输入要求：python 03_download_noaa.py -o  "邮箱地址" -t "2020-07-01 00:00:00 2020-07-01 03:00:00"  (邮件和时间手动指定)
# 输出要求：订单号
# 答题人：(赵少杰)   #此处一定要留下自己的名字###########################


CHROME_DRIVER = 'chromedriver.exe'
URL_NOAA = 'https://www.avl.class.noaa.gov/saa/products/welcome'


class HandleWebDriver:
    def __init__(self):
        # 初始化，浏览器配置
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=self.chrome_options)
        self.driver.maximize_window()

    def handle_noaa(self):
        self.driver.get(URL_NOAA)
        parser = argparse.ArgumentParser(description="get date information from linux command")
        parser.add_argument('-o', default='irycudduff-1569@yopmail.com')
        parser.add_argument('-t', default='2020-07-01 00:00:00 2020-07-01 03:00:00')
        args = parser.parse_args()
        mail_address = args.o
        start_date = str(args.t.split(' ')[0])
        start_time = str(args.t.split(' ')[1])
        end_date = str(args.t.split(' ')[2])
        end_time = str(args.t.split(' ')[3])
        # print(mail_address, start_date, start_time, end_date, end_time)
        # 登陆
        self.driver.find_element_by_xpath('//div[@id="midBlock"]//li[2]/a').click()
        self.driver.find_element_by_xpath('//input[@name="j_username"]').send_keys('irycudduff1')
        self.driver.find_element_by_xpath('//input[@name="j_password"]').send_keys('abc123456')
        self.driver.find_element_by_xpath('//input[@value="Login"]').click()
        # 选择数据
        self.driver.find_element_by_xpath('//select[@name="datatype_family"]//option[@value="IASI3X3"]').click()
        self.driver.find_element_by_xpath('//input[@title="Go to the search page for the selected product"]').click()
        # 选择时间
        self.driver.find_element_by_xpath('//input[@name="start_date"]').clear()
        self.driver.find_element_by_xpath('//input[@name="start_time"]').clear()
        self.driver.find_element_by_xpath('//input[@name="end_date"]').clear()
        self.driver.find_element_by_xpath('//input[@name="end_time"]').clear()
        self.driver.find_element_by_xpath('//input[@name="start_date"]').send_keys(start_date)
        self.driver.find_element_by_xpath('//input[@name="start_time"]').send_keys(start_time)
        self.driver.find_element_by_xpath('//input[@name="end_date"]').send_keys(end_date)
        self.driver.find_element_by_xpath('//input[@name="end_time"]').send_keys(end_time)
        time.sleep(5)
        self.driver.find_element_by_xpath('//input[@id="searchbutton"]').click()
        time.sleep(5)
        # 加购物车
        self.driver.find_element_by_xpath('//select[@name="AddGroup"]/option[last()]').click()
        self.driver.find_element_by_xpath('//input[@value="Goto Cart"]').click()
        # 输入邮箱地址并进行订购
        self.driver.find_element_by_xpath('//input[@name="email"]').clear()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(mail_address)
        self.driver.find_element_by_xpath('//input[@value="PlaceOrder"]').click()
        # 获取订单号
        confirmation_info = self.driver.find_element_by_xpath('//table[@class="class_table center"]//tr/td/text()[3]')[0].strip()
        confirmation_number = confirmation_info.split(':')[1].strip()[:-1]
        print(confirmation_number)


if __name__ == '__main__':
    test_selenium = HandleWebDriver()
    test_selenium.handle_noaa()
