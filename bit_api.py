import requests
import json
import time
import random
import string
from faker import Faker

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}
ip = ''
country = ''
city = ''
postal = ''

# 权重比例和对应的操作系统选项
#os_options = [
#    ('Linux armv81', 4),
#    ('iPhone', 2),
#    ('Win64', 2),
#    ('Win32', 1),
#    ('MacIntel', 0.8),
#    ('Linux x86_64', 0.2)
#]

os_options = [
    ('Linux armv81', 4),
    ('iPhone', 2),
    ('Win64', 2000),
    ('Win32', 1000),
    ('MacIntel', 1000),
    ('Linux x86_64', 0.2)
]

faker = Faker()
webgl_vendors = ['Google Inc.', 'Microsoft',
                 'Apple Inc.', 'ARM', 'Intel Inc.', 'Qualcomm']
webgl_renders = ['ANGLE (Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2070 SUPER Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0)', 'Intel(R) HD Graphics 4600', 'ANGLE (NVIDIA GeForce GTX 750 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K600 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro M1000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon (TM) R9 370 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon HD 7700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'Apple GPU', 'Intel(R) UHD Graphics 620', 'Mali-G72', 'Mali-G72 MP3', 'ANGLE (NVIDIA GeForce GTX 750  Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 750 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 770 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 780 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 850M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 850M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 860M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 950M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 960 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 960M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 960M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 970 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 980 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 980 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 980M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX130 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX150 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX230 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX250 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2060 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce RTX 2060 SUPER Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro FX 380 Direct3D11 vs_4_0 ps_4_0)', 'ANGLE (NVIDIA Quadro NVS 295 Direct3D11 vs_4_0 ps_4_0)', 'ANGLE (NVIDIA Quadro P1000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P2000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P400 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P600 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (ATI Mobility Radeon HD 4330 Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (ATI Mobility Radeon HD 4500 Series Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (ATI Mobility Radeon HD 5000 Series Direct3D11 vs_5_0 ps_5_0)',
                 'ANGLE (ATI Mobility Radeon HD 5400 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8935)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6079)', 'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7870)', 'ANGLE (AMD, Radeon (TM) RX 470 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.1034.6)', 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-10.18.13.6881)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)', 'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.14028.11002)', 'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)', 'ANGLE (AMD, AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13025.1000)', 'ANGLE (AMD, AMD Radeon RX 6900 XT Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13011.1004)', 'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13002.23)', 'ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9466)', 'ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5126)', 'ANGLE (Intel, Intel(R) HD Graphics 6000 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5126)', 'ANGLE (Intel, Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9466)', 'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9168)', 'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6589)', 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9126)', 'ANGLE (Intel, Mesa Intel(R) UHD Graphics 620 (KBL GT2), OpenGL 4.6 (Core Profile) Mesa 21.2.2)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050 Ti/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 460.73.01)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050 Ti/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 460.80)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1060 6GB/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1080 Ti/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1650/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 650/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 750 Ti/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 860M/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 950M/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce MX150/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce RTX 2070/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, NVIDIA GeForce GTX 660/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 470.57.02)', 'ANGLE (NVIDIA Corporation, NVIDIA GeForce RTX 2060 SUPER/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 470.63.01)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll-26.21.14.4250)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 5GB Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7168)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7212)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6677)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7111)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7212)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7111)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7196)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7196)']
color_depths = [1, 2, 3, 4, 5, 8, 12, 15, 16, 18, 24, 30, 32, 48]

# 根据权重选择操作系统
def weighted_random_choice(options):
    total_weight = sum(weight for _, weight in options)
    random_choice = random.uniform(0, total_weight)
    cumulative_weight = 0
    for option, weight in options:
        cumulative_weight += weight
        if random_choice <= cumulative_weight:
            return option

def generate_random_string(length):
    # 生成指定长度的随机字符串，包含字母和数字
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def createBrowser(stay, country_in, offername):  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    # 随机选择代理国家代码
    #country_codes = ['au', 'ca', 'us', 'gb']
    if not stay and offername == 'jerkmate':
        print('selected 1')
        country_codes = ['au', 'ca', 'us', 'gb', 'dk', 'fr', 'is', 'ie', 'it', 'no', 'pr', 'se', 'nz', 'hk', 'jp', 'ch', 'bm', 'cl']
        selected_country_code = random.choice(country_codes)
    elif not stay and offername == 'royalcams':
        print('selected 2')
        #country_codes = ['au', 'ca', 'us', 'gb', 'dk', 'fr', 'it', 'no', 'cs', 'se', 'nz', 'de', 'ee', 'ch', 'be', 'fi', 'il', 'ru']
        country_codes = ['us', 'ca', 'dk', 'fi', 'no', 'ch', 'uk', 'se', 'au']
        selected_country_code = random.choice(country_codes)
    elif not stay and offername == 'bongacams':
        print('selected 3')
        country_codes = ['au', 'ca', 'us', 'gb', 'dk', 'fr', 'it', 'no', 'cs', 'se', 'nz', 'de', 'ee', 'ch', 'be', 'fi']
        selected_country_code = random.choice(country_codes)
    elif not stay and offername == 'cam4':
        print('selected 4')
        country_codes = ['ca', 'us', 'gb', 'fr', 'it', 'se', 'de', 'ch', 'nl']
        selected_country_code = random.choice(country_codes)
    elif not stay and offername == 'Flirtejetzt':
        print('selected 5')
        country_codes = ['at']
        selected_country_code = random.choice(country_codes)
    else:
        selected_country_code = country_in


    # 生成随机字符串
    random_string = generate_random_string(8)  # 生成8位随机字符串，与nnD2H1bq长度相同

    #json_data = {
    #    'name': 'google',  # 窗口名称
    #    'remark': '',  # 备注
    #    'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
    #    # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
    #    'proxyType': 'socks5',
    #    'host': 'geo.iproyal.com',  # 代理主机
    #    'port': '32325',  # 代理端口
	#    'proxyPassword': f'XyPPDxNlMmvxMOGN_country-{selected_country_code}_session-{random_string}_lifetime-24h_streaming-1',
    #    'proxyUserName': 'qKJE32NQAh8KjaON',  # 代理账号
    #    "browserFingerPrint": {  # 指纹对象
    #        'os': weighted_random_choice(os_options),
    #        'userAgent': '',
    #        'coreVersion': '126'  # 内核版本，注意，win7/win8/winserver 2012 已经不支持112及以上内核了，无法打开
    #    }
    #}
    #resolution = random.choice(['1024 x 768', '1280 x 800', '1280 x 960', '1920 x 1080', '1440 x 900', '1280 x 1024'])
    os = weighted_random_choice(os_options)

    if os == 'Linux armv81':
        ostype = 'Android'
        hardwareConcurrency = random.choice([6, 8, 10, 12])
        deviceMemory = random.choice([6, 8, 12])
        resolution = random.choice([
            '1080 x 1920',  # 全高清竖屏
            '1440 x 2560',  # 2K竖屏
            '720 x 1280',   # 常见的720p竖屏
            '1440 x 3040',  # 一些高端手机
            '1080 x 2280',  # 流行的宽高比 19:9
        ])
    elif os == 'iPhone':
        ostype = 'IOS'
        hardwareConcurrency = random.choice([4, 6, 8])
        deviceMemory = random.choice([4, 6, 8])
        resolution = random.choice([
            '828 x 1792',   # iPhone XR
            '1125 x 2436',  # iPhone X, XS
            '1242 x 2688',  # iPhone XS Max
            '1170 x 2532',  # iPhone 12, 12 Pro
            '1284 x 2778',  # iPhone 12 Pro Max
        ])
    else:
        ostype = 'PC'
        hardwareConcurrency = random.choice([4, 6, 8, 12, 16, 18, 24, 32])
        deviceMemory = random.choice([2, 4, 6, 8, 12, 16, 24, 32, 64])
        resolution = random.choice([
            '1920 x 1080',  # 常见的全高清
            '2560 x 1440',  # 2K分辨率
            '1366 x 768',  # 常见的笔记本分辨率
            '1440 x 900',  # 常见的MacBook分辨率
            '1280 x 1024',  # 5:4显示器
            '1680 x 1050',  # 宽屏
        ])

    json_data = {
        "groupId": "",  # 群组ID，绑定群组时传入，如果登录的是子账号，则必须赋值，否则会自动分配到主账户下面去
        "platform": '',  # 账号平台
        "platformIcon": 'other',  # 取账号平台的 hostname 或者设置为other
        "url": '',  # 打开的url，多个用,分开
        "name": 'auto_registry',  # 窗口名称
        # 备注
        "remark": '',
        "userName": '',  # 用户账号
        # "password": password,  # 用户密码
        "password": '',  # 用户密码
        "cookie": '',  # cookie
        "proxyMethod": 2,  # 代理类型 2自定义;3提取IP
        # 自定义代理类型 ['noproxy', 'http', 'https', 'socks5']
        "proxyType": 'socks5',
        #"host": 'geo.iproyal.com',  # 代理主机
        #"port": '32325',  # 代理端口
        #"proxyUserName": 'qKJE32NQAh8KjaON',  # 代理账号
        #"proxyPassword": f'XyPPDxNlMmvxMOGN_country-{selected_country_code}_session-{random_string}_lifetime-24h_streaming-1',  # 代理密码
        #naproxy
        #"host": 'us.naproxy.net',  # 代理主机
        #"port": '1000',  # 代理端口
        #"proxyUserName": f'proxy-ethanxu_area-{selected_country_code}_session-{random_string}_life-120',  # 代理账号
        #"proxyPassword": 'xufuhai111', # 代理密码
        #ipidea
        "host": '51e4f38df2eaf607.na.ipidea.online',  # 代理主机
        "port": '2333',  # 代理端口
        "proxyUserName": f'wumitech_cancer_gray-zone-custom-region-{selected_country_code}-session-{random_string}-sessTime-60',  # 代理账号
        "proxyPassword": 'SA0k8P1VswU',  # 代理密码
        'dynamicIpUrl': '',  # proxyMethod = 3时，提取IP链接
        'dynamicIpChannel': '',  # 提取链接服务商，rola | doveip | cloudam | common
        'isDynamicIpChangeIp': False,  # 每次打开都提取新IP，默认false
        # ip检测服务IP库，默认ip-api，选项 ip-api | ip123in | luminati，luminati为Luminati专用
        'ipCheckService': 'ip-api',
        'isIpv6': False,
        'abortImage': False,  # 是否禁止图片加载
        'abortMedia': False,  # 是否禁止媒体加载
        'stopWhileNetError': False,  # 网络错误时是否停止
        'syncTabs': False,  # 是否同步标签页
        'syncCookies': True,  # 是否同步cookie
        'syncIndexedDb': False,  # 是否同步indexedDB
        'syncBookmarks': True,  # 是否同步书签
        'syncAuthorization': False,  # 是否同步授权
        'syncHistory': True,  # 是否同步历史记录
        'isValidUsername': False,  # 是否验证用户名
        'workbench': 'localserver',
        'allowedSignin': True,  # 允许google账号登录浏览器，默认true
        'syncSessions': False,  # 同步浏览器Sessions，历史记录最近关闭的标签相关，默认false
        'clearCacheFilesBeforeLaunch': False,  # 启动前清理缓存文件，默认false
        "browserFingerPrint": {  # 指纹对象
            'coreVersion': '128',
            'ostype': ostype,  # 操作系统平台 PC|Android|IOS
            'os': os,
            # 为navigator.platform值 Win32 | Linux i686 | Linux armv7l | MacIntel，当ostype设置为IOS时，设置os为iPhone，ostype为Android时，设置为 Linux i686 || Linux armv7l
            'version': str(random.randint(124, 128)),  # 浏览器版本
            'userAgent': '',
            'timeZone': '',  # 时区
            'timeZoneOffset': 0,  # 时区偏移量
            'isIpCreateTimeZone': True,  # 时区
            'webRTC': '0',  # webrtc 0|1|2
            'position': '1',  # 地理位置 0|1|2
            'isIpCreatePosition': True,  # 位置开关
            'lat': '',  # 经度
            'lng': '',  # 纬度
            'precisionData': '',  # 精度米
            'isIpCreateLanguage': True,  # 语言开关
            'languages': '',  # 默认系统
            'isIpCreateDisplayLanguage': True,  # 显示语言默认不跟随IP
            'displayLanguages': '',  # 默认系统
            'resolutionType': '1',  # 分辨
            'resolution': resolution,
            'fontType': '2',  # 字体生成类型
            'font': '',  # 字体
            'canvas': '0',  # canvas
            'canvasValue': random.randint(10000, 1000000),  # canvas 噪音值 10000 - 1000000
            'webGL': '0',  # webGL
            'webGLValue': random.randint(10000, 1000000),  # webGL 噪音值 10000 - 1000000
            'webGLMeta': '0',  # 元数据
            'webGLManufacturer': '',  # 厂商
            'webGLRender': '',  # 渲染
            'audioContext': '0',  # audioContext
            'audioContextValue': random.randint(1, 100),  # audioContext噪音值 1 - 100 ，关闭时默认10
            'mediaDevice': '0',  # mediaDevice
            'mediaDeviceValue': random.randint(1, 100),  # mediaDevice 噪音值，修改时再传回到服务端
            'speechVoices': '0',  # Speech Voices，默认随机
            'speechVoicesValue': random.randint(1, 100),  # peech Voices 值，修改时再传回到服务端
            'hardwareConcurrency': hardwareConcurrency,  # 并发数
            'deviceMemory': deviceMemory,  # 设备内存
            'doNotTrack': '1',  # doNotTrack
            'portScanProtect': '1',  # port
            'portWhiteList': '',
            'colorDepth': random.choice(color_depths),
            'devicePixelRatio': '1.5',
            'openWidth': resolution.split(' x ')[0],
            'openHeight': resolution.split(' x ')[1],
            'ignoreHttpsErrors': True,  # 忽略https证书错误
            'clientRectNoiseEnabled': False,  # 默认关闭
            'clientRectNoiseValue': random.randint(1, 999999),  # 关闭为0，开启时随机 1 - 999999
            'deviceInfoEnabled': True,  # 设备信息，默认关闭
            'computerName': f'Computer-{faker.first_name()}',  # deviceInfoEnabled 为true时，设置
            'macAddr': ('-'.join(['%02x' % faker.pyint(0, 255) for i in range(6)])).upper(),  # deviceInfoEnabled 为true时，设置
            'disableSslCipherSuitesFlag': False, # ssl是否禁用特性，默认不禁用，注意开启后自定义设置时，有可能会导致某些网站无法访问
            'disableSslCipherSuites': None, # ssl禁用特性，序列化的ssl特性值，参考附录
            'enablePlugins': False, # 是否启用插件指纹
            'plugins': '', # enablePlugins为true时，序列化的插件值，插件指纹值参考附录
        }
    }

    #host = json_data['host']
    #proxyPassword = json_data['proxyPassword']
    #proxyUserName = json_data['proxyUserName']
    #port = json_data['port']
    # 代理服务器的地址和认证信息
    #proxy = f'socks5h://{proxyUserName}:{proxyPassword}@{host}:{port}'
    proxy = f'http://165.154.20.60:5000/get_ip_info?location={selected_country_code}&session={random_string}'


    # 目标 URL
    #url_ipinfo = "https://ipinfo.io"

    # 配置代理
    #proxies = {
    #    "http": proxy,
    #    "https": proxy
    #}

    # 发起请求
    #response = requests.get(url_ipinfo, proxies=proxies)
    response = requests.get(proxy)
    global ip
    global country
    global city
    global postal
    ip = response.json()['ip']
    country = response.json()['country']
    city = response.json()['city']
    postal = response.json()['postal']
    print(ip, country, city, postal)

    res = requests.post(f"{url}/browser/update",
                        data=json.dumps(json_data), headers=headers).json()
    #print(res)
    browserId = res['data']['id']
    print(browserId)
    print(res)
    return browserId, ip, country, city, postal, ostype


def updateBrowser():  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
    json_data = {'ids': ['93672cf112a044f08b653cab691216f0'],
                 'remark': '我是一个备注', 'browserFingerPrint': {}}
    res = requests.post(f"{url}/browser/update/partial",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    return res


def closeBrowser(id):  # 关闭窗口
    json_data = {'id': f'{id}'}
    requests.post(f"{url}/browser/close",
                  data=json.dumps(json_data), headers=headers).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {'id': f'{id}'}
    print(requests.post(f"{url}/browser/delete",
          data=json.dumps(json_data), headers=headers).json())

def detailBrowser(id):  # 查询窗口
    json_data = {'id': f'{id}'}
    #print(requests.post(f"{url}/browser/detail",
    #      data=json.dumps(json_data), headers=headers).json())
    return requests.post(f"{url}/browser/detail", data=json.dumps(json_data), headers=headers).json()


if __name__ == '__main__':
    browser_id = createBrowser()
    openBrowser(browser_id)

    time.sleep(10)  # 等待10秒自动关闭窗口

    closeBrowser(browser_id)

    time.sleep(10)  # 等待10秒自动删掉窗口

    deleteBrowser(browser_id)
