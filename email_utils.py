import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import poplib
from email.parser import BytesParser
from email.policy import default
from bs4 import BeautifulSoup
import time

async def extract_confirmation_url(page):
    # 查找包含特定 URL 的第一个链接
    confirmation_link = await page.query_selector('a[href*="https://jerkmatelive.com/signup/confirmEmail/"]')
    if confirmation_link:
        confirmation_url = await confirmation_link.get_attribute('href')
        print(f"Found confirmation URL: {confirmation_url}")
        return confirmation_url
    else:
        print("Confirmation URL not found.")
        return None

async def click_email_and_extract_url(page):
    # 点击包含 "Please activate your account" 的邮件
    email_element = await page.query_selector('text=Please activate your account')
    if email_element:
        await email_element.click()
        await page.wait_for_navigation()  # 等待子页面加载完成
        # 提取确认 URL
        return await extract_confirmation_url(page)
    else:
        print("Email with 'Please activate your account' not found.")

async def check_gmail_for_activation_link(email_user, email_password, revovery_email, page):
    print('check_gmail_for_activation_link')
    await page.goto("https://accounts.google.com/v3/signin/identifier?authuser=0&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ec=GAlAFw&hl=en&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession&dsh=S2132006666%3A1723025337298694&ddm=0", timeout=100000)
    time.sleep(5)
    await page.wait_for_selector('input[type="email"]', timeout=100000)
    await page.fill('input[type="email"]', email_user)
    time.sleep(2)
    await page.wait_for_selector('//button[contains(span, "Next")]', timeout=100000)
    # 在原页面点击链接，触发新标签页打开
    await page.click('//button[contains(span, "Next")]')

    time.sleep(2)
    await page.wait_for_selector('input[type="password"]', timeout=100000)
    await page.fill('input[type="password"]', email_password)
    time.sleep(2)
    await page.wait_for_selector('//button[contains(span, "Next")]', timeout=100000)
    # 在原页面点击链接，触发新标签页打开
    await page.click('//button[contains(span, "Next")]')
    time.sleep(5)
    #await page.click('div.l5PPKe')
    time.sleep(5)
    #await page.wait_for_selector('input[type="email"]', timeout=100000)
    #await page.fill('input[type="email"]', revovery_email)
    time.sleep(2)
    #await page.wait_for_selector('//button[contains(span, "Next")]', timeout=100000)
    # 在原页面点击链接，触发新标签页打开
    #await page.click('//button[contains(span, "Next")]')
    time.sleep(20)
    await page.click('span:has-text("Not now")')
    time.sleep(20)
    await page.click('span:has-text("Not now")')
    time.sleep(20)
    activate_link = await click_email_and_extract_url(page)
    return activate_link

# POP3 检查函数
def check_email_pop3(email_user, email_password):
    pop3_url = 'pop.outlook.com'  # POP3 服务器地址，适用于 Outlook 和 Hotmail
    pop3 = poplib.POP3_SSL(pop3_url)

    printed_links = set()
    relevant_links = []

    try:
        # 登录邮箱账号
        pop3.user(email_user)
        pop3.pass_(email_password)

        # 获取邮件数量
        num_messages = len(pop3.list()[1])

        if num_messages == 0:
            print("POP3: no email")
            return relevant_links

        # 遍历邮件并提取内容和链接
        for i in range(num_messages):
            # 获取邮件
            raw_email = b'\n'.join(pop3.retr(i + 1)[1])
            msg = BytesParser(policy=default).parsebytes(raw_email)

            # 提取邮件正文
            if msg.is_multipart():
                for part in msg.iter_parts():
                    content_type = part.get_content_type()
                    if content_type == 'text/html':
                        html_content = part.get_payload(decode=True).decode()
                        soup = BeautifulSoup(html_content, 'html.parser')
                        links = soup.find_all('a')
                        for link in links:
                            href = link.get('href')
                            if href and is_relevant_link(href) and href not in printed_links:
                                relevant_links.append(href)
                                printed_links.add(href)
            else:
                content_type = msg.get_content_type()
                if content_type == 'text/html':
                    html_content = msg.get_payload(decode=True).decode()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    links = soup.find_all('a')
                    for link in links:
                        href = link.get('href')
                        if href and is_relevant_link(href) and href not in printed_links:
                            relevant_links.append(href)
                            printed_links.add(href)

    except poplib.error_proto as e:
        print(f"POP3 error: {e}")

    finally:
        # 关闭连接
        pop3.quit()

    return relevant_links

# IMAP 检查函数
def check_email_imap(email_user, email_password):
    imap_url = 'imap-mail.outlook.com'  # IMAP 服务器地址，适用于 Outlook 和 Hotmail
    mail = imaplib.IMAP4_SSL(imap_url)

    printed_links = set()
    relevant_links = []

    try:
        # 登录邮箱
        mail.login(email_user, email_password)

        # 遍历收件箱和垃圾邮箱
        folders_to_check = ['INBOX', 'Junk']  # 'Junk' 可能是垃圾邮件的文件夹名称，视服务商而定

        for folder in folders_to_check:
            mail.select(folder)

            # 搜索所有邮件
            result, data = mail.search(None, 'ALL')
            if result != 'OK':
                print(f"Failed to retrieve emails from {folder}")
                continue

            # 获取邮件列表
            email_ids = data[0].split()

            if not email_ids:
                print(f"No emails found in {folder}")
                continue

            # 遍历邮件
            for email_id in email_ids:
                result, message_data = mail.fetch(email_id, '(RFC822)')
                if result != 'OK':
                    print(f"Failed to fetch email with ID {email_id}")
                    continue

                raw_email = message_data[0][1]
                msg = BytesParser(policy=default).parsebytes(raw_email)

                # 检查是否为 multipart 邮件
                if msg.is_multipart():
                    for part in msg.iter_parts():
                        content_type = part.get_content_type()
                        if content_type == 'text/html':
                            html_content = part.get_payload(decode=True).decode()
                            soup = BeautifulSoup(html_content, 'html.parser')
                            links = soup.find_all('a')
                            for link in links:
                                href = link.get('href')
                                if href and is_relevant_link(href) and href not in printed_links:
                                    relevant_links.append(href)
                                    printed_links.add(href)
                else:
                    content_type = msg.get_content_type()
                    if content_type == 'text/html':
                        html_content = msg.get_payload(decode=True).decode()
                        soup = BeautifulSoup(html_content, 'html.parser')
                        links = soup.find_all('a')
                        for link in links:
                            href = link.get('href')
                            if href and is_relevant_link(href) and href not in printed_links:
                                relevant_links.append(href)
                                printed_links.add(href)

    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")

    finally:
        # 关闭连接
        mail.logout()

    return relevant_links

# 主函数：优先尝试 POP3，然后再尝试 IMAP
def check_email_for_activation_link(email_user, email_password):
    # 先尝试使用 POP3
    relevant_links = check_email_pop3(email_user, email_password)

    # 如果 POP3 没有找到链接或没有邮件，改用 IMAP
    if not relevant_links:
        print("No links found with POP3, trying IMAP...")
        relevant_links = check_email_imap(email_user, email_password)

    if not relevant_links:
        print("No activation links found.")
        return 'nothing'

    return relevant_links


# def check_email_for_activation_link(email_user, email_password):
#     # 连接到 POP3 服务器
#     pop3_url = 'pop.outlook.com'  # POP3 服务器地址，适用于 Outlook 和 Hotmail
#     pop3 = poplib.POP3_SSL(pop3_url)
#
#     # 保存已打印的链接
#     printed_links = set()
#     relevant_links = []
#
#     try:
#         # 登录邮箱账号
#         pop3.user(email_user)
#         pop3.pass_(email_password)
#
#         # 获取邮件数量
#         num_messages = len(pop3.list()[1])
#
#         if num_messages == 0:
#             print("has no email")
#             return 'nothing'
#
#         # 遍历邮件并提取内容和链接
#         for i in range(num_messages):
#             # 获取邮件
#             raw_email = b'\n'.join(pop3.retr(i+1)[1])
#             msg = BytesParser(policy=default).parsebytes(raw_email)
#
#             # 提取邮件正文
#             if msg.is_multipart():
#                 for part in msg.iter_parts():
#                     content_type = part.get_content_type()
#                     if content_type == 'text/html':
#                         html_content = part.get_payload(decode=True).decode()
#                         soup = BeautifulSoup(html_content, 'html.parser')
#                         links = soup.find_all('a')
#                         for link in links:
#                             href = link.get('href')
#                             if href and is_relevant_link(href) and href not in printed_links:
#                                 relevant_links.append(href)
#                                 printed_links.add(href)
#             else:
#                 content_type = msg.get_content_type()
#                 if content_type == 'text/html':
#                     html_content = msg.get_payload(decode=True).decode()
#                     soup = BeautifulSoup(html_content, 'html.parser')
#                     links = soup.find_all('a')
#                     for link in links:
#                         href = link.get('href')
#                         if href and is_relevant_link(href) and href not in printed_links:
#                             relevant_links.append(href)
#                             printed_links.add(href)
#
#     except poplib.error_proto as e:
#         print(f"POP3 error: {e}")
#
#     finally:
#         # 关闭连接
#         pop3.quit()

    # 返回符合条件的激活链接
    return relevant_links

def is_relevant_link(href):
    keywords = ['signup', 'confirm', 'email']
    return any(keyword in href for keyword in keywords)

def extract_activation_link(html_content):
    import re
    match = re.search(r'http[s]?://[^\s"]+', html_content)
    return match.group(0) if match else None

def activate_email(activation_link):
    import requests
    response = requests.get(activation_link)
    return response.status_code == 200



