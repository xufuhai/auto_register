from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_ip_info', methods=['GET'])
def get_ip_info():
    # 从请求参数中获取位置和会话
    location = request.args.get('location', default='US', type=str)
    session = request.args.get('session', default='default_session', type=str)

    # 配置代理
    proxy_url = f"proxy-ethanxu_area-{location}_session-{session}_life-5:xufuhai111@us.naproxy.net:1000"
    print(proxy_url)
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        # 发送 GET 请求到 https://ipinfo.io/
        response = requests.get('https://ipinfo.io/', proxies=proxies)
        response.raise_for_status()

        # 返回原始的 JSON 响应
        return jsonify(response.json()), 200
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
