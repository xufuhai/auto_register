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

    print('xufuhaixufuhaibegin')
    # await random_pause()
    # #await page.wait_for_selector('button.align-right.secondary.slidedown-button')
    # # 在原页面点击链接，触发新标签页打开
    # await random_click_element(page, 'button.align-right.secondary.slidedown-button')
    # #await page.wait_for_selector('a[href*="bongacams.com/popular-chat"]', state='visible')
    # # 在原页面点击链接，触发新标签页打开
    # #await random_click_element(page, 'a[href*="bongacams.com/popular-chat"]')
    # await page.wait_for_selector('a[href*="/out/model"]')
    # # 在原页面点击链接，触发新标签页打开
    # await random_click_element(page,'a[href*="/out/model"]')
    # #await page.wait_for_selector('div.profile-img-ctn')
    # await random_pause()
    # await page.reload()
    # await random_click_element(page, 'div.profile-img-ctn')
    # await random_pause()
    # await random_click_element(page, 'img.profile-img')
    # await random_pause()
    # # 在原页面点击链接，触发新标签页打开
    # await random_click_element(page, 'a[href*="/out/homepage"]')
    # #await page.wait_for_selector('a.header-button span')
    # # 在原页面点击链接，触发新标签页打开
    # await random_click_element(page,'a.header-button span')
    # await random_click_element(page, 'a.button-gradient span')
    # print('xufuhaixufuhai')
    # #await wait_for_element_whether_exists(page, "button#answer2")
    # await random_pause()
    # await page.reload()
    # await random_pause()
    # await scroll_page(page, False)
    # await random_pause()
    # await scroll_page(page, False)

    try:
        print('clsoe page and browser')
        await page.close()

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
        #insert_registration_task(url, email.split('_needcheck')[0], password, proxy_ip, user_agent, country, city, 'royalcams')
        pass
    

def close_advertisements(page):
    try:
        page.click('button[class="ad-close"]')
    except:
        pass

def answer_basic_questions(page):
    page.click('button[name="yes_no_1"]')
    page.click('button[name="yes_no_2"]')

def handle_captcha(page):
    pass


browser_id, ip, country, city, postal, ostype = createBrowser(False, '', 'royalcams')
detailes = detailBrowser(browser_id)
#url='https://specdeviceinfo.com/im/click.php?c=2&key=d0kl6o36g3dds3e348ww6ei0'
#url='https://t.ajrkm3.com/334905/8865/33288?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
#url='https://t.ajrkm.link/340062/2994/19129?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
#url='https://t.ajrkm.link/334905/2994/8995?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
url=sys.argv[1]
print(url)
username=generate_username()
#url='https://sweetydating.online/im/click.php?c=17&key=8ql18onn77ez91a7128cz2ga'
if True:
    email = generate_random_email()
else:
    email = get_random_email_with_status_zero('2')
    email = email + '_needcheck'
passwd=generate_password()
#ip=detailes['data']['lastIp']
user_agent=detailes['data']['browserFingerPrint']['userAgent']
#country=''
#city=''
print(email, user_agent, passwd, ip, country, city, postal, username)
register_user_task(url, email, passwd, ip, user_agent, country, city, username, ostype)
