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


async def run(playwright: Playwright, email, username, password, url, ostype):
  #browser_id = createBrowser()
  try:
    # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
    #browser_id = createBrowser()
    global browser_id
    res = openBrowser(browser_id)
    print(res)
    ws = res['data']['ws']
    print("ws address ==>>> ", ws)

    #detailes = detailBrowser(browser_id)
    #userAgent = detailes['data']['browserFingerPrint']['userAgent']
    #ip = detailes['data']['lastIp']
    #print(userAgent)
    #print(ip)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    print('new page and goto baidu')

    page = await default_context.new_page()

    #link = await check_gmail_for_activation_link('lueschenxegaku02@gmail.com', 'IgOAZxYp', 'petrvinogradov2012d3f3m9@yahoo.com', page)
    #print('activate_link:', link)
    #await page.goto(link, timeout=100000)

    await page.goto(url, timeout=150000)

    await random_pause()
    await page.wait_for_selector('button#answer2', state='visible')
    # 在原页面点击链接，触发新标签页打开
    await random_click_element(page,"button#answer2")
    #await wait_for_element_whether_exists(page, "button#answer2")

    await random_pause()
    try:
        await page.wait_for_selector('button#onesignal-slidedown-cancel-button', state='visible')
        await random_click_element(page, 'button#onesignal-slidedown-cancel-button')
    except Exception:
        print("Button not found or not visible. Skipping click.")

    await random_pause()
    await page.wait_for_selector('#cta', timeout=150000)
    # 在原页面点击链接，触发新标签页打开
    await random_click_element(page, "#cta")
    #await wait_for_element_whether_exists(page, "#cta")

    await random_pause()
    # 等待并点击 "NEXT" 按钮
    await page.wait_for_selector('button[type="submit"]', timeout=150000)
    # 等待并填充电子邮件输入字段
    await page.wait_for_selector('input[type="email"]', timeout=150000)
    await page.fill('input[type="email"]', email)
    await random_pause()
    await page.wait_for_selector('input[type="text"]', timeout=150000)
    await page.fill('input[type="text"]', username)
    await random_pause()
    await page.wait_for_selector('input[type="password"]', timeout=150000)
    await page.fill('input[type="password"]', password)
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    time.sleep(15)
    await random_click_element(page, 'button[type="submit"]')
    try:
        #await wait_for_element_whether_exists(page, 'button[type="submit"]')
        try:
            # 等待并点击按钮
            await page.wait_for_selector('button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]', timeout=150000)
            await random_click_element(page, 'button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]')
            #await wait_for_element_whether_exists(page, 'button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]')
            await page.wait_for_selector('[data-ta-locator="AlreadyMemberLogin-Link"]', timeout=150000)
        except Exception:
            # 超时处理
            print("OptionalUpgradeButton or AlreadyMemberLogin Button did not appear within the timeout period.")
        print('ready to check activation_link')
        time.sleep(30)
        if 'gmail' not in email:
            email_passwd = get_email_passwd_with_email(email)
            activate_link = check_email_for_activation_link(email, email_passwd)
            if activate_link == 'nothing':
                closeBrowser(browser_id)
                deleteBrowser(browser_id)
                return 0
            await random_pause()
            await page.goto(activate_link[0], timeout=150000)
        else:
            #email_passwd = get_email_passwd_with_email(email)
            #email_recoveryemail = get_email_passwd_with_recoveryemail(email)
            #activate_link = await check_gmail_for_activation_link(email, email_passwd, email_recoveryemail, page)
            #await page.goto(activate_link, timeout=150000)
            closeBrowser(browser_id)
            return 1

        try:
            # 等待按钮出现，设置超时为 10 秒
            button_selector = 'button[data-ta-locator="AffiliateAgeGateEnterButton"]'
            await page.wait_for_selector(button_selector, state='visible', timeout=10000)

            # 如果按钮出现，点击它
            await random_click_element(page, button_selector)
            print("AffiliateAgeGateEnterButton Button clicked.")
        except Exception:
            # 超时处理
            print("AffiliateAgeGateEnterButton Button did not appear within the timeout period.")

        # 等待并点击 data-ta-locator="CustomLink-FlatButton-startBrowsing-link" 的按钮
        await page.wait_for_selector('[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]', timeout=150000)
        await random_click_element(page, '[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')

        #await wait_for_element_whether_exists(page, '[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')
        random_nums_array = [6, 8, 10, 12, 14, 16, 18, 20]
        random_num = random.choice(random_nums_array)
        print('action random_num:', random_num)
        # 随机点击、随机暂停、返回、滚动
        for _ in range(random_num):  # 进行10次操作，你可以根据需要调整次数
            await random_click(page)
            await random_pause()
            await random_click(page)
            await random_pause()
            if ostype == 'PC':
                await scroll_page(page, False)
            else:
                await scroll_page(page, True)
            await random_pause()
            await random_click(page)
            await random_pause()
            await random_click(page)
            await random_pause()
            if random.random() < 0.4:
                print("Going back and pausing...")
                await page.go_back()
                await random_pause()
            else:
                print("Skipping the go_back and pause actions.")
            #await page.go_back()
            #await random_pause()
            if ostype == 'PC':
                await scroll_page(page, False)
            else:
                await scroll_page(page, True)

        #handle_captcha(page)

        time.sleep(20)

        print('clsoe page and browser')
        await page.close()

        time.sleep(2)
        closeBrowser(browser_id)
        deleteBrowser(browser_id)
        return 1
    except Exception:
        traceback.print_exc()
        deleteBrowser(browser_id)
        return 1
  except Exception:
    traceback.print_exc()
    deleteBrowser(browser_id)
    return 0

async def bit_launch(email, username, password, url, ostype):
    async with async_playwright() as playwright:
      result = await run(playwright, email, username, password, url, ostype)
      return result

@app.task
def register_user_task(url, email, password, proxy_ip, user_agent, country, city, username, ostype):
    print('xufuhai')
    result = asyncio.run(bit_launch(email, username, password, url, ostype))
    if result == 1:
        insert_registration_task(url, email, password, proxy_ip, user_agent, country, city, 'jerkmate')


browser_id, ip, country, city, postal, ostype = createBrowser(False, '')
detailes = detailBrowser(browser_id)
#url='https://specdeviceinfo.com/im/click.php?c=2&key=d0kl6o36g3dds3e348ww6ei0'
#url='https://t.ajrkm3.com/334905/8865/33288?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
url=sys.argv[1]
print(url)
#url='https://sweetydating.online/im/click.php?c=17&key=8ql18onn77ez91a7128cz2ga'
email=get_random_email_with_status_zero('1')
passwd=generate_password()
#ip=detailes['data']['lastIp']
user_agent=detailes['data']['browserFingerPrint']['userAgent']
#country=''
#city=''
username=generate_username()
print(email, user_agent, passwd, ip, country, city, postal, username)
register_user_task(url, email, passwd, ip, user_agent, country, city, username, ostype)
