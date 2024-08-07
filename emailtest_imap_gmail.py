import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

def check_email_for_activation_link(email_user, email_password):
    # 连接到 Gmail IMAP 服务器
    imap_url = 'imap.gmail.com'
    imap = imaplib.IMAP4_SSL(imap_url)

    # 保存已打印的链接
    printed_links = set()
    relevant_links = []

    try:
        # 登录邮箱账号
        imap.login(email_user, email_password)

        # 选择收件箱文件夹
        imap.select('inbox')

        # 搜索未读邮件
        result, data = imap.search(None, 'UNSEEN')
        unseen_messages = data[0].split()

        if not unseen_messages:
            print("没有未读邮件。")
            return []

        # 遍历未读邮件并提取内容和链接
        for message_id in unseen_messages:
            result, message_data = imap.fetch(message_id, '(RFC822)')
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # 提取邮件标题
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            print(f"邮件标题: {subject}")

            # 提取邮件正文
            if msg.is_multipart():
                for part in msg.walk():
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
        # 关闭邮箱连接
        imap.close()
        imap.logout()

    # 返回符合条件的激活链接
    return relevant_links

def is_relevant_link(href):
    keywords = ['signup', 'confirm', 'email']
    return any(keyword in href for keyword in keywords)

link = check_email_for_activation_link('ubbmarkharris636@gmail.com', 'xfh134XUFU!')
print(link[0])
