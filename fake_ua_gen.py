from fake_useragent import UserAgent
import re
import random

def replace_android_version(user_agent, new_versions):
    # 查找 Android 版本号
    match = re.search(r'Android (\d+\.\d+\.\d+|\d+\.\d+|\d+)', user_agent)
    if match:
        current_version = match.group(1)  # 提取当前版本号

        # 计算新的版本号
        new_version = random.choice(new_versions)

        # 替换版本号
        new_user_agent = re.sub(rf'Android {current_version}', f'Android {new_version}', user_agent)
        return new_user_agent
    return user_agent

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


# 生成随机用户代理
ua = UserAgent()
random_ua = ua.random

# 定义新的版本号
new_versions = [125, 126, 127]
android_new_versions = [9, 10, 11, 12, 13, 14]

# 处理用户代理
modified_ua = replace_chrome_version(random_ua, new_versions)

last_ua = replace_android_version(modified_ua, android_new_versions)

print("Modified User-Agent:", last_ua)
