from alibabacloud_cloudauth_intl20220809.client import Client as CloudauthClient
from alibabacloud_cloudauth_intl20220809 import models as cloudauth_models
from alibabacloud_tea_openapi import models as open_api_models
from apps.web.models.auths import (
MetaInfo
    
)

from config import (
    SRC_LOG_LEVELS,
)
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])


class FaceCompare:
    def __init__(self):
        self.config = open_api_models.Config(
            access_key_id='LTAI5tNANMHQzUwyjrcJCv92',
            access_key_secret='JjmtIgPze7r86dn89d8p3i2FMCfhHH',
            endpoint="cloudauth-intl.cn-hongkong.aliyuncs.com"
        )
        
        
#         AccessKey ID
# LTAI5tKRwDnNYRAjF9SkeFv6
# LTAI5tQC7rgovBXLJK9nAh9H

# AccessKey Secret
# 6T5Vf8TNbPJ7fGYREpcZGg9oAYWGde
# y41BCjq6yck32Mw050vGkdMNO8nPqF


        self.client = CloudauthClient(self.config)

    def compare_faces(self, source_face_base64: str, target_face_base64: str):
        print("source_face_base64", 11111)
        request = cloudauth_models.FaceCompareRequest(
            merchant_biz_id="merchant_biz_id_placeholder",
            # source_face_picture=source_face_base64,
            # target_face_picture=target_face_base64
            # source_face_picture_url="https://i.ibb.co/j5pB8jC/example.png",
            # target_face_picture_url="https://i.ibb.co/j5pB8jC/example.png"
            source_face_picture_url="https://testvictor0723.oss-cn-shanghai.aliyuncs.com/face/zhao1.png?Expires=1721877623&OSSAccessKeyId=TMP.3KhtGakqLR3zzecrKbJCKYw4Yi5RzfXj6wqcki8pn8Gu9yaDUFnRdLK3vaPfjieUDWFdZuMTLBm7opzWtFnVHjv9h9jjci&Signature=JvE6dd0nsmYsjfm6x6f%2BFQ9jIak%3D",
            target_face_picture_url="https://testvictor0723.oss-cn-shanghai.aliyuncs.com/face/zhao2.png?Expires=1721877638&OSSAccessKeyId=TMP.3KhtGakqLR3zzecrKbJCKYw4Yi5RzfXj6wqcki8pn8Gu9yaDUFnRdLK3vaPfjieUDWFdZuMTLBm7opzWtFnVHjv9h9jjci&Signature=QoS7Aelvb9XE6QkurxQul3qWjdQ%3D"
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

    def initialize(self, metaInfo: MetaInfo):
        print("metaInfo", metaInfo)
        # 构建初始化请求
        request = cloudauth_models.InitializeRequest(
            merchant_biz_id="c2371516-d114-4872-8de0-b9d2a42f9f7c", #常态，唯一业务标识
            merchant_user_id=metaInfo['user_id'], #动态，用户id
            # meta_info="{\"apdid****mVer\":\"1.0.0\"}", # 动态，传入
            meta_info=str(metaInfo), # 动态，传入

            # return_url="https://www.aliyun.com",
            return_url="https://test.degpt.ai/userVerifying?user_id=" + metaInfo['user_id'],
            # return_url="http://43.242.202.166:3000" ,
            product_code="FACE_LIVENESS",
            security_level="02",
            # languageConfig="****",
            # styleConfig="****",
            # scene_code="****"
        )

        # 调用初始化API
        response = self.client.initialize(request)
        print("initialize_response", response, "https://test.degpt.ai/userVerifying?user_id=" + metaInfo['user_id'])
        return response

    def check_result(self, transaction_id: str, merchant_biz_id: str):
        print("transaction_id: str, merchant_biz_id", transaction_id, merchant_biz_id,)
        
        # 构建结果检查请求
        request = cloudauth_models.CheckResultRequest(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id,
            is_return_image="Y"
        )
  
        # 调用结果检查API
        response = self.client.check_result(request)
        return response

    def face_liveness(self, metaInfo: MetaInfo):
        # 执行初始化
        init_response = self.initialize(metaInfo)
        
        
        # 假设从初始化响应中获取交易ID
        transaction_id = init_response.body.result.transaction_id
        print("transaction_id", transaction_id, init_response, init_response.body.result.transaction_url)
        # merchant_biz_id = init_response.body.result.merchant_biz_id
        merchant_biz_id="c2371516-d114-4872-8de0-b9d2a42f9f7c" #常态，唯一业务标识

        print("merchant_biz_id", merchant_biz_id)
        
        
        
        # 调用结果检查
        # check_response = self.check_result(transaction_id, merchant_biz_id)
        
        return {
            # "initialize_response": init_response,
            "merchant_biz_id":merchant_biz_id,
            "transaction_id": transaction_id,
            "transaction_url":init_response.body.result.transaction_url
            # "check_response": check_response
            
        }




    
    # def ekyc(self, source_face_base64: str, target_face_base64: str):
    #     print("source_face_base64", 11111)
    #     request = cloudauth_models.InitializeRequest(
    #         merchant_biz_id="****",
    #         merchant_user_id="****",
    #         meta_info="{\"apdid****mVer\":\"1.0.0\"}",
    #         returnUrl="****",
    #         authorize="T",
    #         languageConfig="****",
    #         product_code="eKYC"
    #     )
    #     # Invoke API
    #     response = self.client.initialize(request)

    #     # Get result
    #     print(response.status_code)
    #     print(response.body.request_id)
    #     print(response.body.result.transaction_id)
    #     print(response.body.result.transaction_url)

    #     return response
    


    #     # Build request
    #     request = cloudauth_models.CheckResultRequest(
    #         transaction_id="****",
    #         merchant_biz_id="****"
    #     )
 
    #     # Invoke API
    #     response = client.check_result(request)
 
    #     # Get result
    #     print(response.status_code)
    #     print(response.body.request_id)
    #     print(response.body.result.passed)
    #     print(response.body.result.sub_code)
    #     print(response.body.result.ext_face_info)
    #     print(response.body.result.ext_id_info)        






    #     # return "success"

face_compare = FaceCompare()
