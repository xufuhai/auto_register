from fake_useragent import UserAgent
import re
import random


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

# 处理用户代理
modified_ua = replace_chrome_version(random_ua, new_versions)

print("Original User-Agent:", random_ua)
print("Modified User-Agent:", modified_ua)
