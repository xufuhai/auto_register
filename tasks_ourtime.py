from celeryconfig import app
from ai import simulate_human_clicks, simulate_human_actions
from email_utils import check_email_for_activation_link, activate_email
from database import insert_registration_task
from bit_api import *
import time
import asyncio
from playwright.async_api import async_playwright, Playwright
import random
from faker import Faker

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
  await page.wait_for_selector('button#onetrust-accept-btn-handler', state='visible')
  # 在原页面点击链接，触发新标签页打开
  await page.click("#onetrust-accept-btn-handler")
  # 执行点击操作
  time.sleep(3)
  # 或者使用鼠标进行滑动
  await page.mouse.wheel(0, 10000)  # 向下滚动 1000 像素
  time.sleep(1)
  #await page.evaluate("window.scrollTo(0, 100)")
  await page.mouse.wheel(0, -1000)
  time.sleep(1)
  # 执行滑动操作，滚动到页面底部
  await page.mouse.wheel(0, 1000)
  time.sleep(1)
  await page.mouse.wheel(0, -10000)
  
  # 等待选择器加载
  await page.wait_for_selector('select[data-testid="gender-search-profile-select-input"]')
  await page.wait_for_selector('select[data-description = "age-min"]')
  await page.wait_for_selector('select[data-description = "age-max"]')
  await page.wait_for_selector('select[data-testid="gender-search-profile-select-input"]')
  # 等待输入框出现并输入随机城市
  await page.wait_for_selector('input[data-description="location"]')

  # 获取所有option的value
  profile_options = await page.evaluate('''() => {
      const select = document.querySelector('select[data-testid="gender-search-profile-select-input"]');
      return Array.from(select.options).map(option => option.value);
  }''')

  age_min_options = await page.evaluate('''() => {
      const select = document.querySelector('select[data-description = "age-min"]');
      return Array.from(select.options).map(option => option.value);
  }''')

  age_max_options = await page.evaluate('''() => {
        const select = document.querySelector('select[data-description = "age-max"]');
        return Array.from(select.options).map(option => option.value);
    }''')

  # 随机选择一个非默认的option
  random_profile_option = random.choice(profile_options[1:])  # 跳过第一个 "Who are you interested in?"
  random_minage_option = random.choice(age_min_options[1:])
  random_maxage_option = random.choice(age_max_options[1:])

  if random_minage_option > random_maxage_option:
      age_option = random_maxage_option
      random_maxage_option = random_minage_option
      random_minage_option = age_option
  elif random_minage_option == random_maxage_option:
      random_maxage_option = str(int(random_minage_option) + 10)

  # 创建 Faker 实例
  fake = Faker('fr_FR')
  #Faker.seed(0)
  random_city = fake.city()


  # 选择随机选项
  await page.select_option('select[data-testid="gender-search-profile-select-input"]', random_profile_option)
  time.sleep(5)
  await page.select_option('select[data-description = "age-min"]', random_minage_option)
  time.sleep(5)
  await page.select_option('select[data-description = "age-max"]', random_maxage_option)
  time.sleep(5)
  await page.fill('input[data-description="location"]', random_city)
  print(f"Generated Random City: {random_city}")

  # 等待提示列表出现
  await page.wait_for_selector('div[data-description="location-list"] a')

  # 获取所有提示的城市元素
  location_elements = await page.query_selector_all('div[data-description="location-list"] a')

  # 随机选择一个提示的城市并点击
  random_location = random.choice(location_elements)
  await random_location.click()
  time.sleep(3)

  # 等待并点击 "View singles" 按钮
  await page.click('text="View singles"')  # 执行点击操作
  time.sleep(3)


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
  
  time.sleep(20)

  print('clsoe page and browser')
  await page.close()

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
