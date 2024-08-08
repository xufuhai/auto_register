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
        # 判断元素是否是链接，并且target属性是否为'_blank'
        is_link_with_target_blank = await element.evaluate(
            "element => element.tagName === 'A' && element.target === '_blank'"
        )

        if is_visible and is_enabled and not is_link_with_target_blank:
            clickable_and_focusable_elements.append(element)

    return clickable_and_focusable_elements


async def random_click_element(page, selector):
    try:
        # 获取元素
        element = await page.query_selector(selector)
        if element:
            # 获取元素的边界框
            bounding_box = await element.bounding_box()
            if bounding_box:
                # 生成随机点击位置
                start_x = random.uniform(bounding_box['x'], bounding_box['x'] + bounding_box['width'])
                start_y = random.uniform(bounding_box['y'], bounding_box['y'] + bounding_box['height'])

                # 执行点击操作
                await page.mouse.click(start_x, start_y)
                print(f"random_click_element Clicked at ({start_x}, {start_y}) within bounding box: {bounding_box}")
            else:
                print("random_click_element Failed to get bounding box for the element.")
        else:
            print(f"random_click_element Element with selector '{selector}' not found on the page.")

    except Exception as e:
        print(f"random_click_element An error occurred: {e}")

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
                await page.wait_for_timeout(2000)  # 等待2秒，以确保新标签页打开

                # 获取当前所有标签页
                pages = page.context.pages
                print('xufuhai newpage tab num:', pages, len(pages))
                if len(pages) > 1:
                    print('xufuhai enter new pages')
                    # 获取最后打开的标签页，并切换回原始标签页
                    new_tab = pages[-1]
                    print(f"xufuhai check {new_tab} : {original_page}")
                    if new_tab != original_page:
                        print("Switching back to the original tab.")
                        await original_page.bring_to_front()
                        # 关闭新标签页
                        await new_tab.close()
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
        await random_click_element(page, element)
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
        await random_scroll_page(page)
    else:
        await random_scroll_page(page)

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

    await scroll_page(page, False)
    await random_pause()
    await scroll_page(page, False)

    await page.wait_for_selector('a.button-gradient[href^="/out/homepage"]', state='visible')
    # 在原页面点击链接，触发新标签页打开
    await random_click_element(page,'a.button-gradient[href^="/out/homepage"]')
    #await wait_for_element_whether_exists(page, "button#answer2")

    await random_pause()
    await scroll_page(page, False)
    await random_pause()
    await scroll_page(page, False)
    try:
        await page.wait_for_selector('a#btn_signup', state='visible')
        await random_pause()
        await random_click_element(page, 'a#btn_signup')
    except Exception:
        print("Button not found or not visible. Skipping click.")


    await random_pause()
    # 等待并点击 "NEXT" 按钮
    await page.wait_for_selector('button[type="submit"]', timeout=150000)
    # 等待并填充电子邮件输入字段
    await page.wait_for_selector('input[id="user_member_username"]', timeout=150000)
    await page.fill('input[id="user_member_username"]', username)
    await random_pause()
    await page.wait_for_selector('input[id="user_member_email"]', timeout=150000)
    await page.fill('input[id="user_member_email"]', email.split('_needcheck')[0])
    await random_pause()
    await page.wait_for_selector('input[id="user_member_password"]', timeout=150000)
    await page.fill('input[id="user_member_password"]', password)
    await random_pause()
    # 确保复选框元素可见
    await page.wait_for_selector('input#user_member_terms_of_use', state='visible')

    # 选中复选框
    #is_checked = await page.evaluate('document.querySelector("#user_member_terms_of_use").checked')
    #if not is_checked:
    await random_click_element(page, 'input#user_member_terms_of_use')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    await random_pause()
    await random_click_element(page, 'button[type="submit"]')
    time.sleep(15)
    await random_click_element(page, 'button[type="submit"]')
    try:
        # 确保<span>元素可见
        await page.wait_for_selector('span.ace_close', state='visible')
        await random_pause()
        await random_click_element(page, 'span.ace_close')
        print('ready to check activation_link')
        time.sleep(30)

        if 'gmail' not in email:
            if 'needcheck' in email:
                email_passwd = get_email_passwd_with_email(email.split('_needcheck')[0])
                activate_link = check_email_for_activation_link(email.split('_needcheck')[0], email_passwd)
                await page.goto(activate_link[0], timeout=150000)
        else:
            #email_passwd = get_email_passwd_with_email(email)
            #email_recoveryemail = get_email_passwd_with_recoveryemail(email)
            #activate_link = await check_gmail_for_activation_link(email, email_passwd, email_recoveryemail, page)
            #await page.goto(activate_link, timeout=150000)
            pass


        try:
            # 等待按钮出现，设置超时为 10 秒
            button_selector = 'button.dft_hide.popup_hide.__ph_btn.__ph_td'
            await page.wait_for_selector(button_selector, state='visible', timeout=10000)

            # 如果按钮出现，点击它
            await random_click_element(page, button_selector)
            print("button.dft_hide.popup_hide.__ph_btn.__ph_td Button clicked.")
        except Exception:
            # 超时处理
            print("button.dft_hide.popup_hide.__ph_btn.__ph_td Button did not appear within the timeout period.")


        #await wait_for_element_whether_exists(page, '[data-ta-locator="CustomLink-FlatButton-startBrowsing-link"]')


        # 随机点击、随机暂停、返回、滚动
        for _ in range(20):  # 进行10次操作，你可以根据需要调整次数
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

async def bit_launch(email, username, password, url, ostype):
    async with async_playwright() as playwright:
      result = await run(playwright, email, username, password, url, ostype)
      return result

@app.task
def register_user_task(url, email, password, proxy_ip, user_agent, country, city, username, ostype):
    print('xufuhai')
    result = asyncio.run(bit_launch(email, username, password, url, ostype))
    if result == 1:
        insert_registration_task(url, email.split('_needcheck')[0], password, proxy_ip, user_agent, country, city, 'jerkmate')
    

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


# 定义生成随机字符串的函数
def generate_random_prefix(length, username):
    if random.random() < 0.4:
        characters = string.ascii_letters + string.digits
    else:
        if random.random() < 0.4:
            characters = username + string.ascii_letters + string.digits
        else:
            characters = username + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# 定义根据概率生成邮箱的函数
def generate_random_email(username):
    # 定义邮箱域名及其概率
    domains = {
        'outlook': 'outlook.com',
        'hotmail': 'hotmail.com',
        'gmail': 'gmail.com'
    }
    probabilities = {
        'outlook': 5,
        'hotmail': 3,
        'gmail': 2
    }

    # 计算总概率
    total_prob = sum(probabilities.values())

    # 根据概率选择域名
    choice = random.choices(list(domains.keys()), weights=probabilities.values(), k=1)[0]

    # 生成邮箱前缀
    prefix_length = random.randint(6, 12)
    prefix = generate_random_prefix(prefix_length, username)

    # 生成邮箱地址
    email = f"{prefix}@{domains[choice]}"
    return email

browser_id, ip, country, city, postal, ostype = createBrowser()
detailes = detailBrowser(browser_id)
#url='https://specdeviceinfo.com/im/click.php?c=2&key=d0kl6o36g3dds3e348ww6ei0'
#url='https://t.ajrkm3.com/334905/8865/33288?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
url='https://t.ajrkm.link/335292/2994/19129?bo=2779,2778,2777,2776,2775&po=6533&aff_sub5=SF_006OG000004lmDN'
#url=sys.argv[1]
print(url)
username=generate_username()
#url='https://sweetydating.online/im/click.php?c=17&key=8ql18onn77ez91a7128cz2ga'
if random.random() < 0.7:
    email = generate_random_email(username)
else:
    email = get_random_email_with_status_zero()
    email = email + '_needcheck'
passwd=generate_password()
#ip=detailes['data']['lastIp']
user_agent=detailes['data']['browserFingerPrint']['userAgent']
#country=''
#city=''
print(email, user_agent, passwd, ip, country, city, postal, username)
register_user_task(url, email, passwd, ip, user_agent, country, city, username, ostype)
