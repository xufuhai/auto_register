import requests

json_data = {
    'name': 'google',  # 窗口名称
    'remark': '',  # 备注
    'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
    # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
    'proxyType': 'socks5',
    'host': 'geo.iproyal.com',  # 代理主机
    'port': '32325',  # 代理端口
    'proxyPassword': f'XyPPDxNlMmvxMOGN_country-au_session-fasdfadsf_lifetime-24h_streaming-1',
    'proxyUserName': 'qKJE32NQAh8KjaON',  # 代理账号
    "browserFingerPrint": {  # 指纹对象
        'os': '',
        'userAgent': '',
        'coreVersion': '126'  # 内核版本，注意，win7/win8/winserver 2012 已经不支持112及以上内核了，无法打开
    }
}

host = json_data['host']
proxyPassword = json_data['proxyPassword']
proxyUserName = json_data['proxyUserName']
# 代理服务器的地址和认证信息
proxy = f'socks5h://{proxyUserName}:{proxyPassword}@{host}:42325'

# 目标 URL
url = "https://ipinfo.io"

# 配置代理
proxies = {
    "http": proxy,
    "https": proxy
}

# 发起请求
response = requests.get(url, proxies=proxies)

# 输出响应内容
print(response.json())
