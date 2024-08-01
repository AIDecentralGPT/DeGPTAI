from alibabacloud_cloudauth_intl20220809.client import Client as CloudauthClient
from alibabacloud_cloudauth_intl20220809 import models as cloudauth_models
from alibabacloud_tea_openapi import models as open_api_models
from apps.web.models.auths import (
MetaInfo
    
)


class FaceCompare:
    def __init__(self):
        self.config = open_api_models.Config(
            access_key_id='LTAI5tNANMHQzUwyjrcJCv92',
            access_key_secret='JjmtIgPze7r86dn89d8p3i2FMCfhHH',
            endpoint="cloudauth-intl.cn-hongkong.aliyuncs.com"
        )
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
        # # 构建初始化请求
        # request = cloudauth_models.InitializeRequest(
        #     merchant_biz_id="4732897439274329847328979423", #常态，唯一业务标识
        #     merchant_user_id="3213215456486789784567345", #动态，用户id
        #     # meta_info="{\"apdid****mVer\":\"1.0.0\"}", # 动态，传入
        #     meta_info=str(metaInfo), # 动态，传入

        #     # return_url="https://www.aliyun.com",
        #     return_url="http://localhost:5173",
        #     product_code="FACE_LIVENESS",
        #     security_level="02",
        #     # languageConfig="****",
        #     # styleConfig="****",
        #     # scene_code="****"
        #     doc_type="01000000"
        # )

        # print("request", request)

        # # 调用初始化API
        # response = self.client.initialize(request)
        # print("initialize_response", response)




        print("source_face_base64", 11111)
        config = open_api_models.Config(
        access_key_id='LTAI5tNANMHQzUwyjrcJCv92',
        access_key_secret='JjmtIgPze7r86dn89d8p3i2FMCfhHH',
        endpoint="cloudauth-intl.cn-hongkong.aliyuncs.com"
        )
        client = CloudauthClient(config)

        # Build request
        try:
            request = cloudauth_models.InitializeRequest(
            merchant_biz_id="31254325345345345",
            merchant_user_id="58-043085904345890385430",
            meta_info=str(metaInfo),
            return_url="http://localhost:5173",
            authorize="T",
            # languageConfig="****",
            product_code="eKYC",
            security_level="01",
            doc_type="01000000"
            )

            # Invoke API
            response = client.initialize(request)

            # Get result
            print("_____________________________")
            print(response.status_code)
            print(response.body.request_id)
            print(response.body.result.transaction_id)
            print(response.body.result.transaction_url)
            print("_____________________________")
        except Exception as e:
            print("initialize请求报错了呀",e)
            return response
            # return "success"





        return response

    def check_result(self, transaction_id: str, merchant_biz_id: str):
        # 构建结果检查请求
        request = cloudauth_models.CheckResultRequest(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id
        )
        # 调用结果检查API
        response = self.client.check_result(request)
        return response

    def face_liveness(self, metaInfo: MetaInfo):
        # 执行初始化
        print("metaInfo", metaInfo)
        # bioMetaInfo='4.1.0:2916352,0' deviceType='h5' ua='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.153 Mobile/15E148 Safari/604.1'
        init_response = self.initialize(metaInfo)
        #  {'deviceType': 'h5', 'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.153 Mobile/15E148 Safari/604.1', 'bioMetaInfo': '4.1.0:2916352,0'}
        
        
        # 假设从初始化响应中获取交易ID
        transaction_id = init_response.body.result.transaction_id
        print("transaction_id", transaction_id)
        # merchant_biz_id = init_response.body.result.merchant_biz_id
        merchant_biz_id="c2371516-d114-4872-8de0-b9d2a42f9f7c" #常态，唯一业务标识

        print("merchant_biz_id", merchant_biz_id)
        
        # 调用结果检查
        # check_response = self.check_result(transaction_id, merchant_biz_id)
        
        return {
            # "initialize_response": init_response,
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
