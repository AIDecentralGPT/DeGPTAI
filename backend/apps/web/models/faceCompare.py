from alibabacloud_cloudauth_intl20220809.client import Client as CloudauthClient
from alibabacloud_cloudauth_intl20220809 import models as cloudauth_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from apps.web.models.auths import ( MetaInfo )
import time
import os

from config import ( SRC_LOG_LEVELS )
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])

access_key_id = os.getenv("face_access_key_id")
access_key_secret = os.getenv("face_access_key_secret")
endpoint = os.getenv("face_endpoint")
merchant_biz_id = os.getenv("face_merchant_biz_id")
FACE_URL = os.getenv("FACE_URL")

class FaceCompare:
    # 配置请求认证信息
    def __init__(self):
        self.config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint
        )
        
        
        # AccessKey ID
        # LTAI5tKRwDnNYRAjF9SkeFv6
        # LTAI5tQC7rgovBXLJK9nAh9H

        # AccessKey Secret
        # 6T5Vf8TNbPJ7fGYREpcZGg9oAYWGde
        # y41BCjq6yck32Mw050vGkdMNO8nPqF
        self.client = CloudauthClient(self.config)

    # 初始化请求数据
    def initialize(self, metaInfo: MetaInfo):
        print("metaInfo", metaInfo)
        # 构建初始化请求
        timestamp = time.time()
        request = cloudauth_models.InitializeRequest(
            merchant_biz_id=merchant_biz_id, #常态，唯一业务标识
            merchant_user_id=metaInfo['user_id'], #动态，用户id
            # meta_info="{\"apdid****mVer\":\"1.0.0\"}", # 动态，传入
            meta_info=str(metaInfo), # 动态，传入
            # return_url="https://www.aliyun.com",    
            return_url= FACE_URL + "?user_id=" + metaInfo['user_id'] + "&timestamp=" + str(timestamp),
            product_code="FACE_LIVENESS",
            model='PHOTINUS_LIVENESS',
            security_level="02",
            language_config="en"
            # styleConfig="****",
            # scene_code="****"
        )

        # 调用初始化API
        response = self.client.initialize(request)
        return response


    # 获取面容检测连接地址
    def face_liveness(self, metaInfo: MetaInfo):
        # 执行初始化
        init_response = self.initialize(metaInfo)        
        
        # 假设从初始化响应中获取交易ID
        transaction_id = init_response.body.result.transaction_id
        merchant_biz_id=merchant_biz_id #常态，唯一业务标识
        
        return {
            # "initialize_response": init_response,
            "merchant_biz_id":merchant_biz_id,
            "transaction_id": transaction_id,
            "transaction_url":init_response.body.result.transaction_url
            # "check_response": check_response
            
        }

    # 校验人脸检测结果
    def check_result(self, transaction_id: str, merchant_biz_id: str):
        print("transaction_id: str, merchant_biz_id", transaction_id, merchant_biz_id,)

        # faceliveness_check_for_ws c2371516-d114-4872-8de0-b9d2a42f9f7c hks7ac9a85eb8a57caa1044f5778cca6
        # transaction_id: str, merchant_biz_id hks7ac9a85eb8a57caa1044f5778cca6 c2371516-d114-4872-8de0-b9d2a42f9f7c
        # [<alibabacloud_facebody20191230.models.SearchFaceResponseBodyDataMatchList object at 0x7b970617e010>] 181945249
        # face_id 181945249
        # user 0xde184A6809898D81186DeF5C0823d2107c001Da2
        # user_id 181945249 0xde184A6809898D81186DeF5C0823d2107c001Da2
        # passed {'passed': False, 'message': 'Your face has been used'} False
        
        # 构建结果检查请求
        request = cloudauth_models.CheckResultRequest(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id,
            is_return_image="Y"
        )
  
        # 调用结果检查API
        response = self.client.check_result(request)
        print("response.body.request_id", response.body.request_id)
        return response
    
    # 人脸比对
    def compare_faces(self, source_face_base64: str, target_face_base64: str):
        
        request = cloudauth_models.FaceCompareRequest(
            merchant_biz_id = merchant_biz_id,
            source_face_picture = source_face_base64,
            target_face_picture = target_face_base64
        )
        response = self.client.face_compare(request)
        #         # Get result
        # print(response.status_code)
        # print(response.body.request_id)
        # print(response.body.result.transaction_id)
        # print(response.body.result.passed)
        # print(response.body.result.sub_code)

        return response
        # return "success"

face_compare = FaceCompare()
