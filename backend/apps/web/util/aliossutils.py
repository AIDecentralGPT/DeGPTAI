import oss2
import os
import datetime
import uuid
import base64

# 配置访问密钥和Endpoint
access_key_id = os.getenv("FILE_ACCESS_KEY_ID")
access_key_secret = os.getenv("FILE_ACCESS_KEY_SECRET")
endpoint = os.getenv("FILE_HK_ENDPOINT")
bucket_name = os.getenv("FILE_BUCKET_HK_NAME")
oss_url = os.getenv("FILE_OSS_HK_URL")


class AliOssUtils:
    def __init__(self):
        # 创建Bucket对象
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def upload_base64_to_oss(self, base64_str):
        try:
            # 获取当前日期
            now = datetime.datetime.now()
            # 格式化为 年/月/日 形式
            formatted_date = now.strftime("%Y/%m/%d")
            file_name = f"{formatted_date}/audio_{uuid.uuid4()}.wav"

            # 检查并清理 Base64 前缀
            if "," in base64_str:
                base64_str = base64_str.split(",")[1]

            # 解码 Base64 字符串
            audio_data = base64.b64decode(base64_str)

            # 上传到 OSS
            result = self.bucket.put_object(
                file_name, audio_data, headers={"Content-Type": "audio/wav"}
            )

            if result.status == 200:
                return f"{oss_url}{file_name}"
            else:
                return None
        except Exception as e:
            print("==========Oss Upload Error==========:", e)
            return None


AliOSSUtil = AliOssUtils()
