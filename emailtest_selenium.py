import undetected_chromedriver as uc
from selenium import webdriver
# import selenium.webdriver as uc
from selenium.webdriver.common.by import By
import time
from celeryconfig import app
from ai import simulate_human_clicks, simulate_human_actions
from email_utils import check_email_for_activation_link, activate_email, check_email_for_activation_link, check_gmail_for_activation_link
from database import insert_registration_task, get_random_email_with_status_zero, get_email_passwd_with_email, get_email_passwd_with_recoveryemail
from bit_api import *
import time
import asyncio
from playwright.async_api import async_playwright, Playwright
import random
from faker import Faker
import string
import traceback
import sys
from common_function import *
from action import *
from email_random_gen import *
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bit_api import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_gmail_mail(email, password):
    global browser_id
    browser_id, ip, country, city, postal, ostype = createBrowser(False, '', 'FlirteJetzt')
    # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
    res = openBrowser(browser_id) # 窗口ID从窗口配置界面中复制，或者api创建后返回

    print(res)

    driverPath = res['data']['driver']
    debuggerAddress = res['data']['http']

    # selenium 连接代码
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)

    chrome_service = Service(driverPath)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # # 创建 Chrome 浏览器实例
    # options = uc.ChromeOptions()
    #
    # # 添加忽略SSL错误的参数
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--allow-insecure-localhost')  # 可选，忽略本地SSL错误
    # # 启用一些常用的选项，比如禁用自动化检测、无头模式等
    # options.add_argument("--disable-blink-features=AutomationControlled")
    #
    # # 设置 Chrome 浏览器路径（如果你想使用本地已安装的浏览器）
    # # 比如 Mac 上的路径可以是 /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
    # # Windows 的路径例如: "C:/Program Files/Google/Chrome/Application/chrome.exe"
    # options.binary_location = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
    #
    # # 启动 undetected-chromedriver 并且打开指定的 URL
    # driver = uc.Chrome(options=options)
    # 打开Gmail登录页面
    driver.get('https://mail.google.com/')
 
    # 找到用户名输入框并输入用户名
    username_input = driver.find_element(value='identifierId')
    #username = 'nlazurealiso@gmail.com'  # 替换成您的Gmail邮箱地址

    username_input.send_keys(email)
    time.sleep(10)
 
    # 点击“下一步”按钮 VfPpkd-vQzf8d
    next_button = driver.find_element(value='identifierNext')
    next_button.click()
    time.sleep(10)
 
    # 你的邮箱密码
    #password = "Ewscbkout36890"
    password_input = driver.find_element(by=By.NAME, value='Passwd')
    password_input.send_keys(password)
    time.sleep(10)
    # 点击“下一步”按钮
    next_button = driver.find_elements(by=By.TAG_NAME,value='button')
    next_button[1].click()
    print('xufuhai jump')
    driver.get('https://mail.google.com/')
    print('after xufuhai jump')
    time.sleep(10)
    driver.get('https://mail.google.com/')
    time.sleep(20)
    # # 通过 aria-label 定位元素
    # button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Menu"]')
    # # 使用 ActionChains 执行点击操作
    # actions = ActionChains(driver)
    # actions.move_to_element(button).click().perform()
    # time.sleep(20)
    # 使用XPath找到目标元素
    button = driver.find_element(By.XPATH, '//span[@role="button" and @aria-label="More labels"]')

    # 确认元素可见并点击
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
    #time.sleep(10)

    # 执行点击操作
    button.click()
    print("More labels Button clicked successfully.")
    time.sleep(10)
    # 使用XPath找到包含Spam的<a>元素
    spam_link = driver.find_element(By.XPATH, '//a[@aria-label="Spam 1 unread"]')

    # 确认元素可点击
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable(spam_link))

    # 执行点击操作
    spam_link.click()
    print("Spam link clicked successfully.")

    # # 通过 class 定位元素
    # button = driver.find_element(By.CSS_SELECTOR, 'div.CqrfPb.UgTiZc.DxbtB[role="menuitem"]')
    # # 使用 ActionChains 模拟点击
    # actions = ActionChains(driver)
    # actions.move_to_element(button).click().perform()
    # time.sleep(10)

    # 查找包含'the google account team'的div，忽略大小写
    # div_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH,
    #                                     "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'Google')]"))
    # )
    #
    # # 点击找到的元素
    # div_element.click()
    # print("Element containing 'the google account team' clicked successfully.")

    # 获取所有 role="listitem" 的 div 元素
    # 查找 <span> 元素，包含 name="Google"
    # google_element = WebDriverWait(driver, 10).until(
    #     #EC.presence_of_element_located((By.XPATH, "//span[@name='FlirteJetzt']"))
    #     EC.presence_of_element_located((By.XPATH, "//span[@name='Google']"))
    # )
    #
    # # 点击找到的元素
    # google_element.click()
    # 等待用户手动登录或用程序自动登录，然后找到发件人 Google
    # 等待页面加载并找到邮件发件人为 'no-reply@accounts.google.com' 的行
    email_sender_xpath = "//span[@email='mail@flirtejetzt.com']/ancestor::tr"

    # 等待直到邮件元素可见
    email_row = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, email_sender_xpath))
    )
    email_row.click()
    print("Element with name='flirtejetzt' clicked successfully.")
    time.sleep(10)

    # 查找所有 <a> 元素
    links = driver.find_elements(By.TAG_NAME, 'a')

    # 提取所有 <a> 元素的 href 属性值
    href_values = [link.get_attribute('href') for link in links if link.get_attribute('href')]
    return_value = []
    # 打印 href 属性值
    for href in href_values:
        print(href)
        if 'flirtejetzt' in href:
            return_value.append(href)

    print('href_values:', href_values)

    time.sleep(3)
    # 退出
    driver.close()
    driver.quit()
    return return_value[2]

# check_gmail_mail('nlazurealiso@gmail.com', 'Ewscbkout36890')
a = check_gmail_mail('ruhulpollad@gmail.com','0988767890qwwerr')
print('xufuhai:', a)
