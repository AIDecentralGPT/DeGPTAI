import os
import io
import base64
from alibabacloud_facebody20191230.models import CreateFaceDbRequest
from alibabacloud_tea_openapi.models import Config
from alibabacloud_facebody20191230.client import Client
from alibabacloud_tea_util.models import RuntimeOptions
from urllib.request import urlopen
from alibabacloud_facebody20191230.client import Client
from alibabacloud_facebody20191230.models import AddFaceAdvanceRequest
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_facebody20191230.models import SearchFaceRequest

from alibabacloud_facebody20191230.client import Client
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_facebody20191230.models import AddFaceEntityRequest
from alibabacloud_facebody20191230.models import SearchFaceAdvanceRequest
from viapi.fileutils import FileUtils

import configparser
import oss2

from apps.web.models.users import Users

from config import (
    SRC_LOG_LEVELS,
)
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])


class FaceLib:
    def __init__(self):
        self.config = Config(
            # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html。
            # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html。
            # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
            access_key_id='LTAI5tKRwDnNYRAjF9SkeFv6',
            access_key_secret='6T5Vf8TNbPJ7fGYREpcZGg9oAYWGde',
            # 访问的域名
            endpoint='facebody.cn-shanghai.aliyuncs.com',
            # 访问的域名对应的region
            region_id='cn-shanghai'
        )
        
        self.file_utils = FileUtils('LTAI5tKRwDnNYRAjF9SkeFv6', '6T5Vf8TNbPJ7fGYREpcZGg9oAYWGde')


        self.runtime_option = RuntimeOptions()
        self.create_face_db_request = CreateFaceDbRequest(
                    name='Face'
                )
        
        
    def create_face_db(self):
        try:
            # 初始化Client
            client = Client(self.config)
            response = client.create_face_db_with_options(self.create_face_db_request, self.runtime_option)
            # 获取整体结果
            print(response, response.body)
            # [1] {'RequestId': 'BFD1003C-A568-50DD-842C-61B52EA2447C'}
            
            # [1] {'headers': {'date': 'Fri, 02 Aug 2024 09:18:45 GMT', 'content-type': 'application/json;charset=utf-8', 'content-length': '52', 'connection': 'keep-alive', 'keep-alive': 'timeout=25', 'access-control-allow-origin': '*', 'access-control-expose-headers': '*', 'x-acs-request-id': '7F75E7B4-4636-53B4-A8DE-5FC4A9E1F876', 'x-acs-trace-id': 'e5c7f985e0afea44edef6f0ad984d3ab', 'etag': '5TMxmkRtXpXAdkf/r7rDdEA2'}, 'statusCode': 200, 'body': {'RequestId': '7F75E7B4-4636-53B4-A8DE-5FC4A9E1F876'}} {'RequestId': '7F75E7B4-4636-53B4-A8DE-5FC4A9E1F876'}
        except Exception as error:
            # 获取整体报错信息
            print("create_face_db",error)
            # 获取单个字段
            print(error.code)
            # tips: 可通过error.__dict__查看属性名称

                
    def add_face_sample(self, user_id: str):
        try:
            # 初始化Client
            client = Client(self.config)
            add_face_entity_request = AddFaceEntityRequest(
                db_name='Face1',
                entity_id= user_id # 这是userid
            )
            response = client.add_face_entity_with_options(add_face_entity_request, self.runtime_option)
            # 获取整体结果
            print(response.body)
        except Exception as error:
            # 获取整体报错信息
            print(error)
            # 获取单个字段
            print(error.code)
            # tips: 可通过error.__dict__查看属性名称
            
            
    def add_face_data(self, base64_data):
        request = AddFaceAdvanceRequest()
        
        

        #场景一：文件在本地
        #stream = open(r'/tmp/AddFace.jpg', 'rb')
        #request.image_url_object = stream

        #场景二：使用任意可访问的url
        # url = 'https://viapi-test-bj.oss-cn-beijing.aliyuncs.com/viapi-3.0domepic/facebody/AddFace/AddFace.png'
        # img = urlopen(url).read()
        # print('img', img)
        
        
        
        
        
        # 解码Base64数据
        img_data = base64.b64decode(base64_data)

     
        request.image_url_object = io.BytesIO(img_data)
        request.db_name = 'Face1'
        request.entity_id = 'Entity_id'
        request.extra_data = '小明'
        runtime_option = RuntimeOptions()
        try: 
            # 初始化Client
            client = Client(self.config)
            response = client.add_face_advance(request, runtime_option)
            # 获取整体结果
            print(response.body)
        except Exception as error:
            # 获取整体报错信息
            print(error)
            # 获取单个字段
            print(error.code)
            # tips: 可通过error.__dict__查看属性名称


    def uploadImg(self, base64_data):

        # 读取配置文件
        config = configparser.ConfigParser()
        # 假设config.ini位于脚本同级目录下
        config.read('config.ini')

        # 从配置文件中获取Access Key ID和Access Key Secret
        access_key_id = config.get('configName', 'alibaba_cloud_access_key_id')
        access_key_secret = config.get('configName', 'alibaba_cloud_access_key_secret')

        # 使用获取的RAM用户的访问密钥配置访问凭证
        auth = oss2.AuthV4(access_key_id, access_key_secret)




    def search_face(self,base64_data ):
        runtime_option = RuntimeOptions()
        
                # 解码Base64数据
        img_data = base64.b64decode(base64_data)
     
        # request.image_url_object = io.BytesIO(img_data)
        
        search_face_request = SearchFaceAdvanceRequest()
        search_face_request.image_url_object = io.BytesIO(img_data)
        search_face_request.db_name = 'Face1'
        search_face_request.limit = 5

        try:
            # 初始化Client
            client = Client(self.config)
            response = client.search_face_advance(search_face_request, runtime_option)
            # 获取整体结果
            print(response.body.data.match_list, response.body.data.match_list[0].face_items[0].face_id)
            return response.body.data.match_list[0].face_items[0].face_id
        except Exception as error:
            # 获取整体报错信息
            print("search_face error",error)
            # 获取单个字段

    def search_face_user(self,face_id ):
      
        try:
            user_id = Users.get_user_id_by_face_id(face_id)
            return user_id
        except Exception as error:
            # 获取整体报错信息
            print("search_face_user error",error)



face_lib = FaceLib()
