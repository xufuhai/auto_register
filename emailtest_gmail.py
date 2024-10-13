from playwright.async_api import async_playwright
import json

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

# 贝塞尔曲线模拟鼠标移动的函数
def bezier_curve(p0, p1, p2, p3, t):
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t ** 2 * p2
        + t ** 3 * p3
    )

# 模拟自然鼠标移动的函数
async def move_mouse_naturally(page, start_x, start_y, end_x, end_y, steps=20):
    # 随机生成中间控制点
    control_point_1_x = start_x + (end_x - start_x) / 3 + random.uniform(-100, 100)
    control_point_1_y = start_y + (end_y - start_y) / 3 + random.uniform(-100, 100)
    control_point_2_x = start_x + 2 * (end_x - start_x) / 3 + random.uniform(-100, 100)
    control_point_2_y = start_y + 2 * (end_y - start_y) / 3 + random.uniform(-100, 100)

    # 在多个时间点上插值计算贝塞尔曲线位置
    for i in range(steps):
        t = i / steps
        x = bezier_curve(start_x, control_point_1_x, control_point_2_x, end_x, t)
        y = bezier_curve(start_y, control_point_1_y, control_point_2_y, end_y, t)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.01, 0.05))  # 每一步加入随机延迟，模拟真实用户手动操作


# 主点击函数
async def human_like_click(page, selector):
    try:
        # 获取按钮元素
        element = await page.query_selector(selector)
        if not element:
            print(f"Element with selector '{selector}' not found.")
            return

        # 检查按钮是否可见并可点击
        if not (await element.is_visible()):
            print("Button is not visible!")
            return
        if not (await element.is_enabled()):
            print("Button is not enabled!")
            return

        # 获取按钮的边界框
        bounding_box = await element.bounding_box()
        if not bounding_box:
            print("Failed to get bounding box for the element.")
            return

        if not page.viewport_size:
            await page.set_viewport_size({"width": 1280, "height": 720})

        viewport_width = page.viewport_size['width']
        viewport_height = page.viewport_size['height']

        # 在按钮范围内生成随机的点击坐标
        start_x = random.uniform(0, viewport_width)  # 从页面随机位置开始
        start_y = random.uniform(0, viewport_height)
        end_x = random.uniform(bounding_box['x'], bounding_box['x'] + bounding_box['width'])
        end_y = random.uniform(bounding_box['y'], bounding_box['y'] + bounding_box['height'])

        # 模拟自然的鼠标移动
        await move_mouse_naturally(page, start_x, start_y, end_x, end_y)
        await asyncio.sleep(random.uniform(0.5, 1.0))  # 停留0.5到1秒

        # 完整的点击流程，确保触发所有事件
        await page.mouse.down()
        await asyncio.sleep(random.uniform(0.1, 0.5))
        await page.mouse.up()

        print(f"Clicked at ({end_x}, {end_y}) within bounding box: {bounding_box}")

        # 这里等待页面反应或跳转，最多等待10秒
        await page.wait_for_load_state('networkidle', timeout=10000)

    except Exception as e:
        print(f"An error occurred: {e}")

async def login_gmail(page, email, password):
    await page.goto('https://accounts.google.com/')
    await random_pause()
    # 输入邮箱地址
    #await page.fill('input[type="email"]', email)
    #await page.click('button[type="button"]', timeout=30000)  # 点击“下一步”按钮

    #await random_pause()
    #await page.go_back()

    for char in email:
        await page.type('input[type="email"]', char)
        await page.wait_for_timeout(200)
    #await page.fill('input[type="email"]', email)
    await human_like_click(page, 'button[type="button"]')
    #await random_click_element(page, 'button[type="button"]')
    #await page.click('button[type="button"]', timeout=30000)  # 点击“下一步”按钮
    await random_pause()
    # await page.go_back()    # 输入密码
    # await page.fill('input[type="email"]', email)
    # await random_click_element(page, 'button[type="button"]')
    # #await page.click('button[type="button"]', timeout=30000)  # 点击“下一步”按钮
    # await random_pause()
    await page.fill('input[type="password"]', password)
    await random_click_element(page, 'button[type="button"]')
    #await page.evaluate("document.querySelector('button[type=\"button\"]').click()")
    #await page.click('button[type="button"]', timeout=30000)  # 点击“下一步”按钮
    
    # 等待登录成功后的页面加载
    #await page.wait_for_selector('div[aria-label="Primary"]', timeout=30000)

    await page.goto('https://mail.google.com/')

async def read_mail(page, subject):
    # 搜索邮件
    await page.fill('input[name="q"]', subject)  # 在 Gmail 的搜索栏中输入主题
    await page.press('input[name="q"]', 'Enter')

    # 等待搜索结果
    await page.wait_for_selector('tr.zA', timeout=30000)

    # 打开第一封邮件
    await page.click('tr.zA')

    # 读取邮件内容
    email_content = await page.inner_text('div[role="main"]')

    print(f"Email Content: {email_content}")

async def main():
    async with async_playwright() as playwright:
        global browser_id
        browser_id, ip, country, city, postal, ostype = createBrowser(False, '', 'FlirteJetzt')
        #detailes = detailBrowser(browser_id)
        res = openBrowser(browser_id)
        print(res)
        ws = res['data']['ws']
        print("ws address ==>>> ", ws)

        # detailes = detailBrowser(browser_id)
        # userAgent = detailes['data']['browserFingerPrint']['userAgent']
        # ip = detailes['data']['lastIp']
        # print(userAgent)
        # print(ip)

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        print('new page and goto baidu')

        page = await default_context.new_page()

        # link = await check_gmail_for_activation_link('lueschenxegaku02@gmail.com', 'IgOAZxYp', 'petrvinogradov2012d3f3m9@yahoo.com', page)
        # print('activate_link:', link)
        # await page.goto(link, timeout=100000)

        #await page.goto(url, timeout=150000)

        email = 'nlazurealiso@gmail.com'
        password = 'Ewscbkout36890'

        # 登录 Gmail
        await login_gmail(page, email, password)

        # 读取指定主题的邮件内容
        subject = 'Welcome to Gmail'
        await read_mail(page, subject)

        await browser.close()

# 运行代码
import asyncio
asyncio.run(main())

