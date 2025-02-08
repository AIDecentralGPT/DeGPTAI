import urllib, urllib3
import json

AppSecret = "7Xek044qjxFKj9zScHGmYE0mOnGp1dyu"
AppCode = '586e1acb170043c9800d29eead7f6acc'
Url = 'https://fscaptcha.market.alicloudapi.com/'

class CaptchaApi:
    # 获取滑动验证信息
    def checkCaptcha(self, captcha_code: str, client_ip: str) -> bool:
        captcha_json = json.decoder(captcha_code)
        bodys = {}
        http = urllib3.PoolManager()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'APPCODE ' + AppCode
        }
        bodys['CaptchaAppId'] = captcha_json.get('appid')
        bodys['AppSecretKey'] = 'YdjRIVJpEYBPtf5ipiJ3jRm8O'
        bodys['RandStr'] = captcha_json.get('randstr')
        bodys['Ticket'] = captcha_json.get('ticket')
        bodys['UserIp'] = client_ip
        post_data = urllib.parse.urlencode(bodys).encode('utf-8')
        response = http.request('POST', Url, body=post_data, headers=headers)
        content = response.data.decode('utf-8')
        if content:
            return content['CaptchaMsg'] == 'OK'
        else:
            return False

CaptchaApiInstance = CaptchaApi()