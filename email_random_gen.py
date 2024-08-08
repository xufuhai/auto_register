import random
import string

# 定义生成随机字符串的函数
def generate_random_prefix(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 定义根据概率生成邮箱的函数
def generate_random_email():
    # 定义邮箱域名及其概率
    domains = {
        'outlook': 'outlook.com',
        'hotmail': 'hotmail.com',
        'gmail': 'gmail.com'
    }
    probabilities = {
        'outlook': 5,
        'hotmail': 3,
        'gmail': 2
    }
    
    # 计算总概率
    total_prob = sum(probabilities.values())
    
    # 根据概率选择域名
    choice = random.choices(list(domains.keys()), weights=probabilities.values(), k=1)[0]
    
    # 生成邮箱前缀
    prefix_length = random.randint(8, 15)
    prefix = generate_random_prefix(prefix_length)
    
    # 生成邮箱地址
    email = f"{prefix}@{domains[choice]}"
    return email

# 生成一个随机的邮箱地址
random_email = generate_random_email()
print(random_email)

