from celeryconfig import app
from ai import simulate_human_clicks, simulate_human_actions
from email_utils import check_email_for_activation_link, activate_email
from database import insert_registration_task
from bit_api import *
import time
import asyncio
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):

  # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
  browser_id = createBrowser()
  res = openBrowser(browser_id)
  ws = res['data']['ws']
  print("ws address ==>>> ", ws)

  chromium = playwright.chromium
  browser = await chromium.connect_over_cdp(ws)
  default_context = browser.contexts[0]

  print('new page and goto baidu')

  page = await default_context.new_page()

  await page.goto('https://www.ourtime.co.uk/', timeout=100000)

  time.sleep(5)

  async with default_context.expect_page() as new_page_info:
    # 在原页面点击链接，触发新标签页打开
    await page.click('text="Explore"') 
  new_page = await new_page_info.value
  # 执行点击操作
  time.sleep(5)
  # 在新标签页上执行滑动和点击操作
  await new_page.wait_for_load_state()
  time.sleep(5)
  # 或者使用鼠标进行滑动
  await new_page.mouse.wheel(0, 1000)  # 向下滚动 1000 像素
  time.sleep(5)
  # 执行滑动操作，滚动到页面底部
  await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
  time.sleep(5)
  # 或者使用鼠标进行滑动
  await page.mouse.wheel(0, 1000)  # 向下滚动 1000 像素
  time.sleep(5)
  #close_advertisements(page)
  #answer_basic_questions(page)

  #page.fill('input[name="email"]', email)
  #page.fill('input[name="password"]', password)
  #page.fill('input[name="name"]', name)
  #page.fill('input[name="age"]', str(age))
  #page.fill('input[name="location"]', location)
  #page.fill('input[name="zipcode"]', zipcode)

  handle_captcha(page)
  #page.click('button[type="submit"]')

  #simulate_human_clicks(page)
  #simulate_human_actions(page)
  print('ready to check activation_link')
  #activation_link = check_email_for_activation_link('xufuhai1992@gmail.com', 'xfh134XUFU')
  #if activation_link:
  #      activate_email(activation_link)
  
  time.sleep(2)

  print('clsoe page and browser')
  await page.close()
  await new_page.close()

  time.sleep(2)
  closeBrowser(browser_id)
  deleteBrowser(browser_id)

async def bit_launch():
    async with async_playwright() as playwright:
      await run(playwright)

@app.task
def register_user_task(email, password, name, age, location, zipcode):
    proxy_ip = 'http://proxy_ip:proxy_port'
    user_agent = 'your_user_agent'
    country = 'CountryName'
    city = 'CityName'
    print('xufuhai')
    asyncio.run(bit_launch())
    insert_registration_task('https://example.com/register', email, password, proxy_ip, user_agent, country, city)
    

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

register_user_task('example@example.com', 'password123', 'John Doe', 30, 'New York', '10001')
