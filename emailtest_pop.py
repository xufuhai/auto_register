import poplib
from email.parser import BytesParser
from email.policy import default
from bs4 import BeautifulSoup

def check_email_for_activation_link(email_user, email_password):
    # 连接到 POP3 服务器
    pop3_url = 'pop.outlook.com'  # POP3 服务器地址，适用于 Outlook 和 Hotmail
    pop3 = poplib.POP3_SSL(pop3_url)

    # 保存已打印的链接
    printed_links = set()
    relevant_links = []

    try:
        # 登录邮箱账号
        pop3.user(email_user)
        pop3.pass_(email_password)

        # 获取邮件数量
        num_messages = len(pop3.list()[1])

        if num_messages == 0:
            print("没有邮件。")
            return []

        # 遍历邮件并提取内容和链接
        for i in range(num_messages):
            # 获取邮件
            raw_email = b'\n'.join(pop3.retr(i+1)[1])
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

    # 返回符合条件的激活链接
    return relevant_links

def is_relevant_link(href):
    keywords = ['signup', 'confirm', 'email']
    return any(keyword in href for keyword in keywords)

link = check_email_for_activation_link('lkyrccsv28277@hotmail.com', 'FDr38I0q5H')
print(link[0])
