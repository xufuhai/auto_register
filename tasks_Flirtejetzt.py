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

async def run(playwright: Playwright, email, username, password, url, ostype, city, offer):
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

    # 获取最终重定向后的URL
    final_url = page.url
    print(f"Final URL after redirection: {final_url}")
    last_url = re.sub(r'landing\d+', 'landing2', final_url)

    await page.goto(last_url, timeout=150000)

    await scroll_page(page, False)
    await random_pause()
    await scroll_page(page, False)
    await random_pause()
    print('xufuhaixufuhaibegin')
    #await page.reload()
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
        if ostype == 'PC':
            print("xufuhaixufuhai")
            await random_pause()
            #await page.wait_for_selector('div.RegistrationForm__buttonContainer__Ey9jH', state='visible')
            await page.wait_for_selector('button.sso.lt_button_next.sso-button-email')
            await random_click_element(page, 'button.sso.lt_button_next.sso-button-email')
            #await page.click('button[data-id="Create Free Account"]')
            print("xufuhaixufuhai1")
            await random_pause()
            #await random_click_element(page, 'a.bt30.bt30_green.bc_uppercase.join_btn')
            #await random_pause()
            #await random_click_element(page, 'a.bt30.bt30_green.bc_uppercase.join_btn')
            #print("xufuhaixufuhai2")
        else:
            print("xufuhaixufuhai")
            await random_pause()
            #await page.wait_for_selector('div.RegistrationForm__buttonContainer__Ey9jH', state='visible')
            await page.wait_for_selector('button.sso.lt_button_next.sso-button-email')
            await random_click_element(page, 'button.sso.lt_button_next.sso-button-email')
            #await page.click('button[data-id="Create Free Account"]')
            print("xufuhaixufuhai1")
            await random_pause()
            #await random_click_element(page, 'a.join-btn.ui-btn.ui-btn-up-f.ui-shadow.ui-btn-corner-all')
            #await random_pause()
            #await random_click_element(page, 'a.join-btn.ui-btn.ui-btn-up-f.ui-shadow.ui-btn-corner-all')
            #print("xufuhaixufuhai2")

    except Exception:
        print("Button not found or not visible. Skipping click.")

    await random_pause()
    # 等待并点击 "NEXT" 按钮
    # await page.wait_for_selector('button[type="submit"]', timeout=150000)
    # 等待并填充电子邮件输入字段
    print("xufuhaixufuhai3")
    selectors = [
         'button.button.female.noaccent',
         'button.button.male'
    ]
    gendor = random.choice(selectors)
    await random_click_element(page, gendor)
    print('fsaffdsf')
    await random_pause()
    #await page.hover('button[data-i18n="landing2-button-yes"]')
    #await page.click('button[data-i18n="landing2-button-yes"]')
    selectors = [
        'button[data-i18n="landing2-button-no"]',
        'button[data-i18n="landing2-button-yes"]'
    ]
    yesorno = random.choice(selectors)
    await page.evaluate("(selector) => document.querySelector(selector).click()", yesorno)

    #await random_click_element(page, 'button[data-i18n="landing2-button-no"]')
    #await page.click('button[data-i18n="landing2-button-no"]')
    #await page.click('button[data-next=""]')
    await random_pause()
    #await random_pause()
    #await page.hover('button[data-i18n="landing2-button-yes"]')
    #await page.click('button[data-i18n="landing2-button-yes"]')
    selectors = [
        'button[data-i18n="landing2-button-no"]',
        'button[data-i18n="landing2-button-yes"]'
    ]
    yesorno = random.choice(selectors)
    await page.evaluate("(selector) => document.querySelector(selector).click()", yesorno)
    #await page.click('button[data-i18n="landing2-button-yes"]')
    #await random_click_element(page, 'button[data-i18n="landing2-button-no"]')
    #await page.click('button[data-next=""]')
    await random_pause()
    print('xufuhaixufuhai')
    await page.wait_for_selector('input[data-field="city"]', timeout=150000)
    # 逐个字符输入
    for char in city[:4]:
        await page.type('input[data-field="city"]', char)
        await page.wait_for_timeout(100)  # 模拟每个字符之间的延迟
    # await page.fill('input[data-field="city"]', city)
    # await random_pause()
    # await page.fill('input[data-field="city"]', city[:4])
    # await random_pause()
    # await page.fill('input[data-field="city"]', city[:2])
    await page.wait_for_selector('#location-suggest li')
    cities = await page.query_selector_all('#location-suggest li')
    random_city = random.choice(cities)
    await random_city.click()
    await random_pause()
    #await random_click_element(page, 'button.lt_button_next')
    await page.evaluate("document.querySelector('button.lt_button_next').click()")

    await page.wait_for_selector('input#lt_input_username', timeout=150000)
    #num_arrays = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    #usernum = random.choice(num_arrays)
    #await page.fill('input#lt_input_username', username)
    for char in username:
        await page.type('input#lt_input_username', char)
        await page.wait_for_timeout(100)  # 模拟每个字符之间的延迟
    # await page.wait_for_selector('input#user_member_username, input#log_in_username, input[name="log_in[username]"], input[name="user_member[username]"]', timeout=150000)
    # await page.fill('input#user_member_username, input#log_in_username, input[name="log_in[username]"], input[name="user_member[username]"]', username)
    await random_pause()
    #await random_click_element(page, 'button.lt_button_next')
    await page.evaluate("document.querySelector('button.lt_button_next').click()")

    #await random_click_element(page, 'button.bt30.bt30_green.next')
    #await random_pause()

    # await page.wait_for_selector('input#registration-email', timeout=150000)
    # await page.fill('input#registration-email', email)
    # await random_pause()
    # await random_click_element(page, 'button.lt_button_next')


    # await page.wait_for_selector('input[id="user_member_email"]', timeout=150000)
    # await page.fill('input[id="user_member_email"]', email.split('_needcheck')[0])
    # await random_pause()
    # await page.wait_for_selector('input#user_member_password, input#log_in_password, input[name="log_in[password]"], input[name="user_member[password]"]', timeout=150000)
    # await page.fill('input#user_member_password, input#log_in_password, input[name="log_in[password]"], input[name="user_member[password]"]', password)
    await page.wait_for_selector('input#lt_input_password', timeout=150000)
    #await page.fill('input#lt_input_password', password)
    for char in password:
        await page.type('input#lt_input_password', char)
        await page.wait_for_timeout(100)  # 模拟每个字符之间的延迟
    await random_pause()
    #await random_click_element(page, 'button.lt_button_next')
    await page.evaluate("document.querySelector('button.lt_button_next').click()")

    #选日
    await page.wait_for_selector('#lt_select_dateday')
    options = await page.query_selector_all('#lt_select_dateday option')
    available_options = [option for option in options if await option.get_attribute('value')]
    random_option = random.choice(available_options)
    value = await random_option.get_attribute('value')
    await page.select_option('#lt_select_dateday', value)
    await random_pause()

    #选月
    await page.wait_for_selector('#lt_select_datemonth')
    options = await page.query_selector_all('#lt_select_datemonth option')
    available_options = [option for option in options if await option.get_attribute('value')]
    random_option = random.choice(available_options)
    value = await random_option.get_attribute('value')
    await page.select_option('#lt_select_datemonth', value)
    await random_pause()

    #选年
    await page.wait_for_selector('#lt_select_dateyear')
    options = await page.query_selector_all('#lt_select_dateyear option')
    available_options = [option for option in options if await option.get_attribute('value')]
    random_option = random.choice(available_options)
    value = await random_option.get_attribute('value')
    await page.select_option('#lt_select_dateyear', value)
    await random_pause()
    #await random_click_element(page, 'button.lt_button_next')
    await page.evaluate("document.querySelector('button.lt_button_next').click()")


    await page.wait_for_selector('input#lt_input_email', timeout=150000)
    await page.fill('input#lt_input_email', email)
    await random_pause()
    #await random_click_element(page, 'button.lt_button_next')
    await page.evaluate("document.querySelector('button.lt_button_next').click()")
    # 确保复选框元素可见
    # await page.wait_for_selector('span.ui-icon.ui-icon-checkbox-off.ui-icon-shadow', state='visible')

    # 选中复选框
    # is_checked = await page.evaluate('document.querySelector("#user_member_terms_of_use").checked')
    # if not is_checked:

    # 确保复选框元素可见
    # await random_click_element(page, 'span.ui-icon.ui-icon-checkbox-off.ui-icon-shadow')
    await random_click_element(page, 'input.cc-tickbox-input')
    #await page.check('input#registration-consent-checkbox')
    await random_pause()
    await random_click_element(page, 'input.cc-tickbox-input')
    await random_pause()
    #await random_click_element(page, 'input#registration-terms-consent-checkbox')
    #await page.check('input#registration-terms-consent-checkbox')
    #await random_pause()
    await random_click_element(page, 'button#lt_button_confirm')
    # await random_click_element(page, 'button.bt30.bt30_green.bt_green_solid')
    await random_pause()
    await random_click_element(page, 'button#lt_button_confirm')
    await random_pause()
    # await random_click_element(page, 'button[type="submit"]')
    #await random_click_element(page, 'button.bt30.bt30_green.bt_green_solid')
    #await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    #await random_click_element(page, 'button.bt30.bt30_green.bt_green_solid')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    await random_pause()
    #print('xufuhai ready recaptcha')
    #await random_click_element(page, 'span#recaptcha-anchor')
    #await random_click_element(page, 'button.join_submit.bt30.bt30_green')
    time.sleep(15)
    # await random_click_element(page, 'button[type="submit"]')

    # await random_click(page)
    # await random_pause()
    # await page.goto('https://royalcams.com/', timeout=150000)
    # await random_pause()
    # await random_click_element(page, 'button.buytokens_tablet')
    # await random_pause()
    # await random_click(page)
    # await random_pause()

    #await page.wait_for_selector('input[name="email"]', timeout=150000)
    #await page.fill('input[name="email"]', email.split('_needcheck')[0])

    try:
        # 确保<span>元素可见
        # await page.wait_for_selector('span.vpe_fit_text.js-fit_text', state='visible')
        # await random_pause()
        # await random_click_element(page, 'span.vpe_close')
        # await random_pause()
        # await random_click_element(page, 'a.bc_btn.bc_btn_green.hcb_btn')
        # await random_pause()
        # await random_click_element(page, 'button.bc_btn.bc_btn_green.hcb_btn')
        # await random_pause()
        # await random_click_element(page, 'button.join_submit.bt30.bt30_green')
        # await random_pause()
        # await random_click_element(page, 'button[type="submit"]')
        # await random_pause()
        # await random_click_element(page, 'span.vpe_fit_text.js-fit_text')
        # await random_pause()
        # await random_click_element(page, 'span.vpe_close')
        await random_pause()
        #print('xufuhai ready close verifyemaisent')
        #await random_click_element(page, 'button#jtymt23l_VerifyEmailSent_closeBtn')
        print('ready to check activation_link')
        time.sleep(30)

        if 'gmail' not in email:
            email_passwd = get_email_passwd_with_email(email)
            activate_link = check_email_for_activation_link(email, email_passwd, offer)
            print('activate_link:', activate_link)
            if activate_link == 'nothing':
                closeBrowser(browser_id)
                deleteBrowser(browser_id)
                return 0
            await random_pause()
            await page.goto(activate_link[0], timeout=150000)
        else:
            # email_passwd = get_email_passwd_with_email(email)
            # email_recoveryemail = get_email_passwd_with_recoveryemail(email)
            # activate_link = await check_gmail_for_activation_link(email, email_passwd, email_recoveryemail, page)
            # await page.goto(activate_link, timeout=150000)
            closeBrowser(browser_id)
            return 1

        # await random_pause()
        # selectors = [
        #     'a[href="/all"]',
        #     'a[href="/male"]',
        #     'a[href="/female"]',
        #     'a[href="/transgender"]'
        # ]
        # gendor = random.choice(selectors)
        # await random_click_element(page, gendor)
        # await random_pause()
        # await wait_for_element_whether_exists(page, '[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')
        time.sleep(30)
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'label.cc-radio-label-confirm')
        await random_pause()
        await random_click_element(page, 'div.button.button-allow')
        await random_pause()


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
                # await page.goto('https://royalcams.com/', timeout=150000)
                # await random_pause()
            else:
                print("Skipping the go_back and pause actions.")
            # await page.go_back()
            # await random_pause()
            if ostype == 'PC':
                await scroll_page(page, False)
            else:
                await scroll_page(page, True)

        handle_captcha(page)

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

async def bit_launch(email, username, password, url, ostype, city, offer):
    async with async_playwright() as playwright:
      result = await run(playwright, email, username, password, url, ostype, city, offer)
      return result

@app.task
def register_user_task(url, email, password, proxy_ip, user_agent, country, city, username, ostype):
    print('xufuhai')
    result = asyncio.run(bit_launch(email, username, password, url, ostype, city, 'FlirteJetzt'))
    if result == 1:
        insert_registration_task(url, email, password, proxy_ip, user_agent, country, city, 'FlirteJetzt')
    

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


browser_id, ip, country, city, postal, ostype = createBrowser(False, '', 'FlirteJetzt')
detailes = detailBrowser(browser_id)
#url='https://specdeviceinfo.com/im/click.php?c=2&key=d0kl6o36g3dds3e348ww6ei0'
#url='https://t.ajrkm3.com/334905/8865/33288?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
#url='https://t.ajrkm.link/340062/2994/19129?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
#url='https://t.antj.link/340059/9388/35674?bo=2753,2754,2755,2756&po=6456&aff_sub5=SF_006OG000004lmDN'
url='https://t.antj.link/340059/9388/35674?bo=2753,2754,2755,2756&po=6456&aff_sub5=SF_006OG000004lmDN'
#url=sys.argv[1]
print(url)
username=generate_username()
#url='https://sweetydating.online/im/click.php?c=17&key=8ql18onn77ez91a7128cz2ga'
email = get_random_email_with_status_zero('5')
passwd=generate_password()
#ip=detailes['data']['lastIp']
user_agent=detailes['data']['browserFingerPrint']['userAgent']
#country=''
#city=''
print(email, user_agent, passwd, ip, country, city, postal, username)
register_user_task(url, email, passwd, ip, user_agent, country, city, username, ostype)
