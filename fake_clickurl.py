import requests
import random
import string
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from fake_useragent import UserAgent
import re

# 随机生成8位字符串
def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_string(length):
    # 生成指定长度的随机字符串，包含字母和数字
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

random_string = generate_random_string(8)  # 生成8位随机字符串，与nnD2H1bq长度相同

# 随机选择国家代码
def random_country_code():
    country_codes = ['au', 'ca', 'us', 'gb', 'dk', 'fr', 'is', 'ie', 'it', 'no', 'pr', 'se', 'nz', 'hk', 'jp', 'bm', 'cl']
    return random.choice(country_codes)

# 根据国家代码选择语言
def country_to_language(country_code):
    languages = {
        'au': 'en-AU',
        'ca': 'en-CA',
        'us': 'en-US',
        'gb': 'en-GB',
        'dk': 'da-DK',
        'fr': 'fr-FR',
        'is': 'is-IS',
        'ie': 'en-IE',
        'it': 'it-IT',
        'no': 'no-NO',
        'pr': 'pt-PT',
        'se': 'sv-SE',
        'nz': 'en-NZ',
        'hk': 'zh-HK',
        'jp': 'ja-JP',
        'cn': 'zh-CN',
        'bm': 'en-BM',
        'cl': 'es-CL',
        'ch': 'de-CH'  # 瑞士的语言代码
    }
    return languages.get(country_code, 'en-US')

# 创建 UserAgent 实例，配置不同操作系统和软件
def get_random_user_agent(software_name, operating_system):
    user_agent_rotator = UserAgent(software_name=software_name, operating_system=operating_system)
    return user_agent_rotator.get_random_user_agent()

def replace_chrome_version(user_agent, new_versions):
    # 查找 Chrome 版本号
    match = re.search(r'Chrome/(\d+)\.(\d+)\.(\d+)\.(\d+)', user_agent)
    if match:
        major_version = int(match.group(1))  # 提取主版本号

        # 计算替换的新版本号
        new_major_version = random.choice(new_versions)

        # 替换主版本号
        new_user_agent = re.sub(rf'Chrome/{major_version}', f'Chrome/{new_major_version}', user_agent)
        return new_user_agent
    return user_agent


def replace_android_version(user_agent, new_versions):
    # 查找 Android 版本号
    match = re.search(r'Android (\d+)', user_agent)
    if match:
        current_version = int(match.group(1))  # 提取当前版本号

        # 计算新的版本号
        new_version = random.choice(new_versions)

        # 替换版本号
        new_user_agent = re.sub(rf'Android {current_version}', f'Android {new_version}', user_agent)
        return new_user_agent
    return user_agent

os = ['Windows', 'Mac', 'Android', 'iOS', 'Linux']

# 生成随机用户代理
ua = UserAgent()
random_ua = ua.random

# 定义新的版本号
new_versions = [125, 126, 127]
android_new_versions = [9, 10, 11, 12, 13, 14]
# 处理用户代理
modified_ua = replace_chrome_version(random_ua, new_versions)
last_ua = replace_android_version(modified_ua, android_new_versions)

def generate_user_agents():
    user_agents = {
        'Windows': get_random_user_agent(SoftwareName.CHROME, OperatingSystem.WINDOWS),
        'Mac': get_random_user_agent(SoftwareName.CHROME, OperatingSystem.MAC),
        'Android': get_random_user_agent(SoftwareName.CHROME, OperatingSystem.ANDROID),
        'iOS': get_random_user_agent(SoftwareName.CHROME, OperatingSystem.IOS),
        'Linux': get_random_user_agent(SoftwareName.CHROME, OperatingSystem.LINUX)
    }
    return user_agents

# 随机选择 User-Agent
def random_user_agent():
    agents = {
        'android': [
            "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ1A.200205.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; Galaxy S21 Ultra 5G Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
        ],
        'ios': [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.6 Mobile/15E148 Safari/604.1"
        ],
        'mac': [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        ],
        'windows': [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"
        ],
        'linux': [
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
    }
    os_type = random.choice(list(agents.keys()))
    return random.choice(agents[os_type])

# 随机化 SOCKS5 代理的字段
country_code = random_country_code()
proxy_url = f"socks5h://qKJE32NQAh8KjaON:XyPPDxNlMmvxMOGN_country-{country_code}_session-{random_string}_lifetime-24h_streaming-1@geo.iproyal.com:42325"
# 请求的 URL
url = 'https://specdeviceinfo.com/im/click.php?c=5&key=2teof463dta75hnlt292iamf'

# 配置 User-Agent 和其他头信息
headers = {
    'User-Agent': last_ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'Accept': 'application/json',
    'Accept-Language': f"{country_to_language(country_code)},{country_to_language(country_code).split('-')[0]};q=0.9",
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://specdeviceinfo.com'
}


# 目标 URL
#url_ipinfo = "https://ipinfo.io"

# 配置代理
#proxies = {
#    "http": proxy_url,
#    "https": proxy_url
#}

# 发起请求
#response = requests.get(url_ipinfo, proxies=proxies)
#global ip
#global country
#global city
#global postal
#ip = response.json()['ip']
#country = response.json()['country']
#city = response.json()['city']
#postal = response.json()['postal']
#print('ipinfo:', ip, country, city, postal)
print(proxy_url)
print(country_code)
print(random_string)
print(last_ua)
print(country_to_language(country_code), country_to_language(country_code).split('-')[0])
print(headers)
# 发送请求
try:
    response = requests.get(url, headers=headers, proxies={"http": proxy_url, "https": proxy_url}, allow_redirects=True, timeout=30)
    response.raise_for_status()  # 检查请求是否成功
except Exception:
    # 处理超时异常
    print("Request timed out.")

print(response.content)
# 打印结果
print(f"Total Size: {len(response.content)} bytes")

