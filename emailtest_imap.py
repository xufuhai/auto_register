import imaplib
import email
from bs4 import BeautifulSoup
from email_utils import *


# def check_email_for_activation_link(email_user, email_password):
#     # 连接到Outlook邮箱服务器
#     imap_url = 'imap.outlook.com'
#     imap = imaplib.IMAP4_SSL(imap_url)
#
#     # 保存已打印的链接
#     printed_links = set()
#     relevant_links = []
#
#     try:
#         # 登录邮箱账号
#         imap.login(email_user, email_password)
#
#         # 选择收件箱文件夹
#         imap.select('Inbox')
#
#         # 搜索未读邮件
#         result, data = imap.uid('search', None, '(UNSEEN)')
#         unseen_messages = data[0].split()
#
#         if not unseen_messages:
#             print("没有未读邮件。")
#             return []
#
#         # 遍历未读邮件并提取内容和链接
#         for message_id in unseen_messages:
#             result, message_data = imap.uid('fetch', message_id, '(RFC822)')
#             raw_email = message_data[0][1]
#             msg = email.message_from_bytes(raw_email)
#
#             # 提取邮件正文
#             if msg.is_multipart():
#                 for part in msg.walk():
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
#     except imaplib.IMAP4.error as e:
#         print(f"IMAP error: {e}")
#
#     finally:
#         # 关闭邮箱连接
#         imap.close()
#         imap.logout()
#
#     # 返回符合条件的激活链接
#     return relevant_links

# def check_email_for_activation_link(email_user, email_password):
#     # 先尝试使用 POP3
#     relevant_links = check_email_pop3(email_user, email_password)
#
#     # 如果 POP3 没有找到链接或没有邮件，改用 IMAP
#     if not relevant_links:
#         print("No links found with POP3, trying IMAP...")
#         relevant_links = check_email_imap(email_user, email_password)
#
#     if not relevant_links:
#         print("No activation links found.")
#         return 'nothing'
#
#     return relevant_links
#
# def is_relevant_link(url):
#     # 只选择包含 "signup"、"confirm" 或 "email" 的链接，且链接较长
#     return any(keyword in url for keyword in ['signup', 'confirm', 'email']) and len(url) > 50

link = check_email_for_activation_link('rjnpcpx9pzh@outlook.com', 'M5XyAwXvi88')
print(link[0])
