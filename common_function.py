from faker import Faker
import string
import random
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