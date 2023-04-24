import ssl,OpenSSL,socket
import datetime,time
import requests

# 飞书Webhook参数
webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/58902552-2ddd-41d8-aa54-9193c5fdffb2'
# SSL证书参数
domains = [ 'pc.yueyouxs.cn','tjshuchen.com','m.suixkan.com','ios.biqugogo.com','davinci.c3.biqugogo.com','jump.yueyouxs.com' ]

# 获取证书信息并检查到期时间
ssl_context = ssl.create_default_context()
for domain in domains:
    try:
        with ssl_context.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            not_after = cert['notAfter']

        # 解析日期时间
        not_after_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')

        # 计算天数
        days_left = (not_after_date - datetime.datetime.now()).days

        # 发送提醒消息
        if days_left <= 45:
            message = f'{domain} 的证书将于 {not_after_date} 到期，还有 {days_left} 天。请尽快更新证书。'
            headers = {'Content-Type': 'application/json'}
            data = {'msg_type': 'text', 'content': {'text': message}}
            response = requests.post(webhook_url, headers=headers, json=data)
            if response.status_code != 200:
                print(f'Failed to send alert message for {domain}: {response.text}')
            else:
                print(f'Alert message for {domain} sent successfully.')
    except Exception as e:
        print(f'Failed to get SSL certificate information for {domain}: {str(e)}')

