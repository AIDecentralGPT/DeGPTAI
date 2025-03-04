from alibabacloud_cloudauth_intl20220809.client import Client as CloudauthClient
from alibabacloud_cloudauth_intl20220809 import models as cloudauth_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from apps.web.models.auths import ( MetaInfo )
import time

from config import ( SRC_LOG_LEVELS, FACE_URL )
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])

class FaceCompare:
    # Configure request authentication information
    def __init__(self):
        self.config = open_api_models.Config(
            access_key_id='*******************',
            access_key_secret='**********************',
            endpoint="cloudauth-intl.cn-hongkong.aliyuncs.com"
        )
        
        
        # AccessKey ID
        # LTAI5tKRwDnNYRAjF9SkeFv6
        # LTAI5tQC7rgovBXLJK9nAh9H

        # AccessKey Secret
        # 6T5Vf8TNbPJ7fGYREpcZGg9oAYWGde
        # y41BCjq6yck32Mw050vGkdMNO8nPqF
        self.client = CloudauthClient(self.config)

    # Initialize request data
    def initialize(self, metaInfo: MetaInfo):
        print("metaInfo", metaInfo)
        # Build initialization request
        timestamp = time.time()
        request = cloudauth_models.InitializeRequest(
            merchant_biz_id="c2371516-d114-4872-8de0-b9d2a42f9f7c", #Normal, unique business identifier
            merchant_user_id=metaInfo['user_id'], #Dynamic, user ID
            # meta_info="{\"apdid****mVer\":\"1.0.0\"}", # Dynamic, incoming
            meta_info=str(metaInfo), # Dynamic, incoming
            # return_url="https://www.aliyun.com",    
            return_url= FACE_URL + "?user_id=" + metaInfo['user_id'] + "&timestamp=" + str(timestamp),
            product_code="FACE_LIVENESS",
            model='PHOTINUS_LIVENESS',
            security_level="02",
            language_config="en"
            # styleConfig="****",
            # scene_code="****"
        )

        # Call initialization API
        response = self.client.initialize(request)
        return response


    # Obtain the connection address for facial detection
    def face_liveness(self, metaInfo: MetaInfo):
        # Perform initialization
        init_response = self.initialize(metaInfo)        
        
        # Assuming to obtain the transaction ID from the initialization response
        transaction_id = init_response.body.result.transaction_id
        merchant_biz_id="c2371516-d114-4872-8de0-b9d2a42f9f7c" #Normal, unique business identifier
        
        return {
            # "initialize_response": init_response,
            "merchant_biz_id":merchant_biz_id,
            "transaction_id": transaction_id,
            "transaction_url":init_response.body.result.transaction_url
            # "check_response": check_response
            
        }

    # Verify facial detection results
    def check_result(self, transaction_id: str, merchant_biz_id: str):
        print("transaction_id: str, merchant_biz_id", transaction_id, merchant_biz_id,)

        # faceliveness_check_for_ws c2371516-d114-4872-8de0-b9d2a42f9f7c hks7ac9a85eb8a57caa1044f5778cca6
        # transaction_id: str, merchant_biz_id hks7ac9a85eb8a57caa1044f5778cca6 c2371516-d114-4872-8de0-b9d2a42f9f7c
        # [<alibabacloud_facebody20191230.models.SearchFaceResponseBodyDataMatchList object at 0x7b970617e010>] 181945249
        # face_id 181945249
        # user 0xde184A6809898D81186DeF5C0823d2107c001Da2
        # user_id 181945249 0xde184A6809898D81186DeF5C0823d2107c001Da2
        # passed {'passed': False, 'message': 'Your face has been used'} False
        
        # Build result check request
        request = cloudauth_models.CheckResultRequest(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id,
            is_return_image="Y"
        )
  
        # Call result check API
        response = self.client.check_result(request)
        print("response.body.request_id", response.body.request_id)
        return response
    
    # Facial comparison
    def compare_faces(self, source_face_base64: str, target_face_base64: str):
        
        request = cloudauth_models.FaceCompareRequest(
            merchant_biz_id = "c2371516-d114-4872-8de0-b9d2a42f9f7c",
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
