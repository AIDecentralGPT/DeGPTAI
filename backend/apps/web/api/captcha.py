import urllib, urllib3
import json
import os

AppSecret = os.getenv("CaptchaAppSecret")
AppCode = os.getenv("CaptchaAppCode")
Url = os.getenv("CaptchaUrl")

class CaptchaApi:
    # 获取滑动验证信息
    def checkCaptcha(self, captcha_code: str, client_ip: str) -> bool:
        captcha_json = json.loads(captcha_code)
        bodys = {}
        http = urllib3.PoolManager()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'APPCODE ' + AppCode
        }
        bodys['CaptchaAppId'] = captcha_json.get('appid')
        bodys['AppSecretKey'] = AppSecret
        bodys['RandStr'] = captcha_json.get('randstr')
        bodys['Ticket'] = captcha_json.get('ticket')
        bodys['UserIp'] = client_ip
        post_data = urllib.parse.urlencode(bodys).encode('utf-8')
        response = http.request('POST', Url, body=post_data, headers=headers)
        content = response.data.decode('utf-8')
        if content:
            content_json = json.loads(content)
            if content_json.get("code") == "200":
                return content_json.get("data").get("CaptchaMsg") == 'OK'
            else:
                return False
        else:
            return False

CaptchaApiInstance = CaptchaApi()