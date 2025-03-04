import io
import base64
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_facebody20191230.models import CreateFaceDbRequest, AddFaceEntityRequest, GetFaceEntityRequest, AddFaceAdvanceRequest, SearchFaceAdvanceRequest, DeleteFaceRequest, DetectLivingFaceRequest, DetectLivingFaceRequestTasks
from alibabacloud_facebody20191230.client import Client 
from viapi.fileutils import FileUtils

from apps.web.models.users import Users

import os

from config import (
    SRC_LOG_LEVELS
)
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])

FACE_DB = os.getenv("FACE_DB")
ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET")
ENDPOINT = os.getenv("OSS_ENDPOINT")
REGION_ID = os.getenv("OSS_REGION_ID")

class FaceLib:
    def __init__(self):
        self.faceDb = FACE_DB
        self.config = Config(
            # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html。
            # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html。
            # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
            access_key_id=ACCESS_KEY_ID,
            access_key_secret=ACCESS_KEY_SECRET,
            # 访问的域名
            endpoint=ENDPOINT,
            # 访问的域名对应的region
            region_id=REGION_ID
        )

        self.runtime_option = RuntimeOptions()
        self.create_face_db_request = CreateFaceDbRequest( name=self.faceDb )

        # 阿里oss上传文件
        self.file_utils = FileUtils(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        
    # 创建人脸数据库
    def create_face_db(self):
        try:
            # 初始化Client
            client = Client(self.config)
            response = client.create_face_db_with_options(self.create_face_db_request, self.runtime_option)
            return response;
        except Exception as error:
            return error;

    # 添加人脸样本 再 添加 人脸数据
    def add_face_sample(self, user_id):
        request = AddFaceEntityRequest()
        request.db_name = self.faceDb
        request.entity_id = user_id
        request.labels = "face-sample"
        try: 
            # 初始化Client
            client = Client(self.config)
            response = client.add_face_entity_with_options(request, self.runtime_option)
            # 获取整体结果
            print(response)
        except Exception as error:
            # 获取整体报错信息
            print(error)

    # 获取人脸样本
    def get_face_sample(self, user_id):
        request = GetFaceEntityRequest()
        request.db_name = self.faceDb
        request.entity_id = user_id
        try: 
            # 初始化Client
            client = Client(self.config)
            response = client.get_face_entity_with_options(request, self.runtime_option)
            # 获取整体结果
            print(response)
        except Exception as error:
            # 获取整体报错信息
            print(error)
            
    # 添加人脸数据
    def add_face_data(self, base64_data, user_id):
        request = AddFaceAdvanceRequest()       
        # 解码Base64数据
        img_data = base64.b64decode(base64_data)
        request.image_url_object = io.BytesIO(img_data)
        request.db_name = self.faceDb
        request.entity_id = user_id
        request.extra_data = 'degpt-face:' + user_id
        try: 
            # 初始化Client
            client = Client(self.config)
            response = client.add_face_advance(request, self.runtime_option)
            # 获取整体结果
            print(response.body)
            return response.body.data.face_id
        except Exception as error:
            # 获取整体报错信息
            print(error)
            return ""

    # 检索人脸数据
    def search_face(self, base64_data ):
        runtime_option = RuntimeOptions()
        
        # 解码Base64数据
        img_data = base64.b64decode(base64_data)
     
        # request.image_url_object = io.BytesIO(img_data)
        
        search_face_request = SearchFaceAdvanceRequest()
        search_face_request.image_url_object = io.BytesIO(img_data)
        search_face_request.db_name = self.faceDb
        search_face_request.limit = 5
        
        try:
            # 初始化Client
            client = Client(self.config)
            response = client.search_face_advance(search_face_request, runtime_option)
            # 获取整体结果
            print("获取人脸匹配数据结果:", response.body.data)
            match_list = response.body.data.match_list
            if (len(match_list) > 0 and len(match_list[0].face_items) > 0):
                for item in match_list[0].face_items:
                    if (item.score > 0.65):
                        return item.face_id
            # 没有返回face_id 返回None
            return None
        except Exception as error:
            # 获取整体报错信息
            print("search_face error",error)
            # 获取单个字段

    # 删除人脸数据
    def remove_face(self, face_id):

        deleteFaceRequest = DeleteFaceRequest()
        deleteFaceRequest.db_name = self.faceDb
        deleteFaceRequest.face_id = face_id

        runtime_option = RuntimeOptions()

        try:
            # 初始化Client
            client = Client(self.config)
            response = client.delete_face_with_options_async(deleteFaceRequest, runtime_option)
            # 获取整体结果
            print(response.body)
        except Exception as error:
            # 获取整体报错信息
            print(error)
            # 获取单个字段

    # 通过人脸ID检索用户信息
    def search_face_user(self, face_id):   
        try:
            user_id = Users.get_user_id_by_face_id(face_id)
            return user_id
        except Exception as error:
            # 获取整体报错信息
            print("search_face_user error",error)

    # 校验人脸的来源真实性
    def check_face_image(self, face_base64: str):
        # 初始化Client
        client = Client(self.config)
        # 构建结果检查请求
        try:
            detect_living_face_request = DetectLivingFaceRequest(tasks=[DetectLivingFaceRequestTasks(image_data=face_base64)])
            response= client.detect_living_face_with_options(detect_living_face_request, self.runtime_option)
            print("============check_face_image==============", response.body.data)
            if response.body.data.elements[0].results[0].suggestion == 'pass':
                return True
            else:
                return False
        except Exception as error:
            print("============check_face_image==============", error)
            return False

face_lib = FaceLib()
