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

# 生成随机用户名
def generate_username():
    fake = Faker()
    return fake.user_name()


# 生成随机密码
def generate_password(min_length=9, max_length=14):
    if min_length < 8:
        raise ValueError("Minimum password length should be at least 8 characters")

    # 定义字符集
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    punctuation = string.punctuation.replace("'", "").replace('"', "")  # 去掉单引号和双引号

    # 至少一个字符的不同类别
    required_chars = [
        random.choice(uppercase),  # 至少一个大写字母
        random.choice(lowercase),  # 至少一个小写字母
        random.choice(digits),  # 至少一个数字
        random.choice(punctuation)  # 至少一个特殊字符
    ]

    # 随机长度
    password_length = random.randint(min_length, max_length)

    # 剩余的字符长度
    remaining_length = password_length - len(required_chars)

    # 生成剩余字符
    remaining_chars = random.choices(uppercase + lowercase + digits + punctuation, k=remaining_length)

    # 组合所有字符
    password_chars = required_chars + remaining_chars

    # 打乱密码字符顺序
    random.shuffle(password_chars)

    # 确保特殊字符和数字不在开头
    while any(c in digits + punctuation for c in password_chars[:2]):
        random.shuffle(password_chars)

    return ''.join(password_chars)


async def get_clickable_and_focusable_elements(page):
    # 使用可见性过滤器获取当前可见的可点击元素
    elements = await page.locator(
        "button, [role='button'], a, [onclick], input[type='button'], input[type='submit']"
    ).all()

    clickable_and_focusable_elements = []

    for element in elements:
        is_visible = await element.is_visible()
        is_enabled = await element.is_enabled()
        if is_visible and is_enabled:
            clickable_and_focusable_elements.append(element)

    return clickable_and_focusable_elements
async def random_click(page):
    try:
        # 获取当前窗口的句柄
        original_page = page

        # 获取页面上所有可点击的元素
        clickable_elements = await get_clickable_and_focusable_elements(page)

        if clickable_elements:
            # 随机选择一个可点击的元素
            element = random.choice(clickable_elements)
            # 获取元素的位置信息
            bounding_box = await element.bounding_box()
            if bounding_box:
                # 随机生成点击点
                x = random.uniform(bounding_box['x'], bounding_box['x'] + bounding_box['width'])
                y = random.uniform(bounding_box['y'], bounding_box['y'] + bounding_box['height'])

                # 滚动到随机点击点
                await page.evaluate(f"window.scrollTo({x}, {y})")
                await asyncio.sleep(random.uniform(1, 2))  # 停顿一下，模拟人类滚动

                # 点击随机点
                await page.mouse.click(x, y)
                print(f"Clicked on random point ({x}, {y}) within bounding box: {bounding_box}")

                # 检查是否打开了新的标签页
                async def switch_to_original_tab():
                    nonlocal original_page
                    pages = await page.context.pages()
                    if len(pages) > 1:
                        # 获取最后打开的标签页，并切换回原始标签页
                        for p in pages:
                            if p != original_page:
                                print("Switching back to the original tab.")
                                await original_page.bring_to_front()
                                break

                await switch_to_original_tab()

            else:
                print("Failed to get bounding box for the element.")
        else:
            print("No clickable elements found on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def random_pause():
    # 随机暂停1到10秒
    pause_time = random.uniform(2, 5)
    print(f"Pausing for {pause_time:.2f} seconds")
    await asyncio.sleep(pause_time)

async def wait_for_element_whether_exists(page, element):
    submit_button = await page.query_selector(element)
    print(submit_button, element)
    if submit_button and await submit_button.is_visible():
        time.sleep(5)
        await page.click(element)
        time.sleep(5)


async def random_scroll_page(page):
    try:
        # 获取页面的总高度
        body_handle = await page.query_selector('body')
        body_box = await body_handle.bounding_box()
        total_height = body_box['height']

        # 随机生成滑动的起点和终点
        start_y = random.uniform(0, total_height - 100)  # 保证滑动不会超出页面
        end_y = random.uniform(start_y, total_height)
        start_x = random.uniform(0, body_box['width'])  # 随机水平位置
        end_x = start_x  # 垂直滑动，不改变水平位置

        # 执行滚动操作
        await page.evaluate(f"window.scrollTo({start_x}, {start_y})")
        await asyncio.sleep(random.uniform(1, 2))  # 模拟人类滚动
        await page.evaluate(f"window.scrollTo({start_x}, {end_y})")

        print(f"Scrolled from ({start_x}, {start_y}) to ({end_x}, {end_y}) on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def random_touch_scroll_page(page):
    try:
        # 获取页面的总高度
        body_handle = await page.query_selector('body')
        body_box = await body_handle.bounding_box()
        total_height = body_box['height']

        # 随机生成滑动的起点和终点
        start_y = random.uniform(0, total_height - 100)  # 保证滑动不会超出页面
        end_y = random.uniform(start_y, total_height)
        start_x = random.uniform(0, body_box['width'])  # 随机水平位置
        end_x = start_x  # 垂直滑动，不改变水平位置

        # 执行触控滑动操作
        await page.touchscreen.tap(start_x, start_y)
        await asyncio.sleep(random.uniform(0.5, 1))
        await page.touchscreen.swipe(start_x, start_y, end_x, end_y)

        print(f"Scrolled from ({start_x}, {start_y}) to ({end_x}, {end_y}) on the page.")

    except Exception as e:
        print(f"An error occurred: {e}")


async def scroll_page(page, is_mobile: bool):
    if is_mobile:
        await random_touch_scroll_page(page)
    else:
        await random_scroll_page(page)

async def run(playwright: Playwright, email, username, password, url):
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

    await page.goto(url, timeout=100000)

    random_pause()
    await page.wait_for_selector('button#answer2', state='visible')
    # 在原页面点击链接，触发新标签页打开
    await page.click("button#answer2")
    #await wait_for_element_whether_exists(page, "button#answer2")

    random_pause()
    await page.wait_for_selector('button#onesignal-slidedown-cancel-button', state='visible')
    await page.click('button#onesignal-slidedown-cancel-button')
    random_pause()
    await page.wait_for_selector('#cta', timeout=100000)
    # 在原页面点击链接，触发新标签页打开
    await page.click("#cta")
    #await wait_for_element_whether_exists(page, "#cta")

    random_pause()
    # 等待并点击 "NEXT" 按钮
    await page.wait_for_selector('button[type="submit"]', timeout=100000)
    # 等待并填充电子邮件输入字段
    await page.wait_for_selector('input[type="email"]', timeout=100000)
    await page.fill('input[type="email"]', email)
    random_pause()
    await page.wait_for_selector('input[type="text"]', timeout=100000)
    await page.fill('input[type="text"]', username)
    random_pause()
    await page.wait_for_selector('input[type="password"]', timeout=100000)
    await page.fill('input[type="password"]', password)
    random_pause()
    await page.click('button[type="submit"]')
    try:
        #await wait_for_element_whether_exists(page, 'button[type="submit"]')
        # 等待并点击按钮
        await page.wait_for_selector('button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]', timeout=100000)
        await page.click('button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]')

        #await wait_for_element_whether_exists(page, 'button[data-ta-locator="FreemiumSignup-OptionalUpgradeButton"]')

        await page.wait_for_selector('[data-ta-locator="AlreadyMemberLogin-Link"]', timeout=100000)
        print('ready to check activation_link')
        time.sleep(30)
        if 'gmail' not in email:
            email_passwd = get_email_passwd_with_email(email)
            activate_link = check_email_for_activation_link(email, email_passwd)
            await page.goto(activate_link[0], timeout=100000)
        else:
            email_passwd = get_email_passwd_with_email(email)
            email_recoveryemail = get_email_passwd_with_recoveryemail(email)
            activate_link = await check_gmail_for_activation_link(email, email_passwd, email_recoveryemail, page)
            await page.goto(activate_link, timeout=100000)

        # 等待并点击 data-ta-locator="CustomLink-FlatButton-startBrowsing-link" 的按钮
        await page.wait_for_selector('[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]', timeout=100000)
        await page.click('[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')

        #await wait_for_element_whether_exists(page, '[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')


        # 随机点击、随机暂停、返回、滚动
        for _ in range(20):  # 进行10次操作，你可以根据需要调整次数
            await random_click(page)
            await random_pause()
            await random_click(page)
            await random_pause()
            await scroll_page(page, True)
            await random_pause()
            await random_click(page)
            await random_pause()
            await random_click(page)
            await random_pause()
            if random.random() < 0.2:
                print("Going back and pausing...")
                await page.go_back()
                await random_pause()
            else:
                print("Skipping the go_back and pause actions.")
            #await page.go_back()
            #await random_pause()
            await scroll_page(page, False)

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

async def bit_launch(email, username, password, url):
    async with async_playwright() as playwright:
      result = await run(playwright, email, username, password, url)
      return result

@app.task
def register_user_task(url, email, password, proxy_ip, user_agent, country, city, username):
    print('xufuhai')
    result = asyncio.run(bit_launch(email, username, password, url))
    if result == 1:
        insert_registration_task(url, email, password, proxy_ip, user_agent, country, city, 'jerkmate')
    

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


browser_id, ip, country, city, postal = createBrowser()
detailes = detailBrowser(browser_id)
url='https://specdeviceinfo.com/im/click.php?c=2&key=d0kl6o36g3dds3e348ww6ei0'
#url='https://t.ajrkm3.com/334905/8865/33288?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
email=get_random_email_with_status_zero()
passwd=generate_password()
#ip=detailes['data']['lastIp']
user_agent=detailes['data']['browserFingerPrint']['userAgent']
#country=''
#city=''
username=generate_username()
print(email, user_agent, passwd, ip, country, city, postal, username)
register_user_task(url, email, passwd, ip, user_agent, country, city, username)
