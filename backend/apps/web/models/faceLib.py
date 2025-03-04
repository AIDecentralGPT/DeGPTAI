import io
import base64
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_facebody20191230.models import CreateFaceDbRequest, AddFaceEntityRequest, GetFaceEntityRequest, AddFaceAdvanceRequest, SearchFaceAdvanceRequest, DeleteFaceRequest, DetectLivingFaceRequest, DetectLivingFaceRequestTasks
from alibabacloud_facebody20191230.client import Client 
from viapi.fileutils import FileUtils

from apps.web.models.users import Users

from config import (
    SRC_LOG_LEVELS,
    FACE_DB
)
import logging
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["faceCompare"])

class FaceLib:
    def __init__(self):
        self.faceDb = FACE_DB
        self.config = Config(
            access_key_id='******************',
            access_key_secret='*******************',
            # Visited Domain Name
            endpoint='facebody.cn-shanghai.aliyuncs.com',
            # The region corresponding to the accessed domain name
            region_id='cn-shanghai'
        )

        self.runtime_option = RuntimeOptions()
        self.create_face_db_request = CreateFaceDbRequest( name=self.faceDb )

        # Upload files on Alibaba OSS
        self.file_utils = FileUtils('**************', '*******************************')
        
    # Create a facial database
    def create_face_db(self):
        try:
            # Initialize client
            client = Client(self.config)
            response = client.create_face_db_with_options(self.create_face_db_request, self.runtime_option)
            return response;
        except Exception as error:
            return error;

    # Add face samples and then add face data
    def add_face_sample(self, user_id):
        request = AddFaceEntityRequest()
        request.db_name = self.faceDb
        request.entity_id = user_id
        request.labels = "face-sample"
        try: 
            # Initialize client
            client = Client(self.config)
            response = client.add_face_entity_with_options(request, self.runtime_option)
            # Obtain overall results
            print(response)
        except Exception as error:
            # Obtain overall error information
            print(error)

    # Obtain facial samples
    def get_face_sample(self, user_id):
        request = GetFaceEntityRequest()
        request.db_name = self.faceDb
        request.entity_id = user_id
        try: 
            # Initialize client
            client = Client(self.config)
            response = client.get_face_entity_with_options(request, self.runtime_option)
            # Obtain overall results
            print(response)
        except Exception as error:
            # Obtain overall error information
            print(error)
            
    # Add facial data
    def add_face_data(self, base64_data, user_id):
        request = AddFaceAdvanceRequest()       
        # Decoding Base64 data
        img_data = base64.b64decode(base64_data)
        request.image_url_object = io.BytesIO(img_data)
        request.db_name = self.faceDb
        request.entity_id = user_id
        request.extra_data = 'degpt-face:' + user_id
        try: 
            # Initialize client
            client = Client(self.config)
            response = client.add_face_advance(request, self.runtime_option)
            # Obtain overall results
            print(response.body)
            return response.body.data.face_id
        except Exception as error:
            # Obtain overall error information
            print(error)
            return ""

    # Retrieve facial data
    def search_face(self, base64_data ):
        runtime_option = RuntimeOptions()
        
        # Decoding Base64 data
        img_data = base64.b64decode(base64_data)
     
        # request.image_url_object = io.BytesIO(img_data)
        
        search_face_request = SearchFaceAdvanceRequest()
        search_face_request.image_url_object = io.BytesIO(img_data)
        search_face_request.db_name = self.faceDb
        search_face_request.limit = 5
        
        try:
            # Initialize client
            client = Client(self.config)
            response = client.search_face_advance(search_face_request, runtime_option)
            # Obtain overall results
            print("Obtain facial matching data results:", response.body.data)
            match_list = response.body.data.match_list
            if (len(match_list) > 0 and len(match_list[0].face_items) > 0):
                for item in match_list[0].face_items:
                    if (item.score > 0.65):
                        return item.face_id
            # No face_id returned, None returned
            return None
        except Exception as error:
            # Obtain overall error information
            print("search_face error",error)
            # Get a single field

    # Delete facial data
    def remove_face(self, face_id):

        deleteFaceRequest = DeleteFaceRequest()
        deleteFaceRequest.db_name = self.faceDb
        deleteFaceRequest.face_id = face_id

        runtime_option = RuntimeOptions()

        try:
            # Initialize client
            client = Client(self.config)
            response = client.delete_face_with_options_async(deleteFaceRequest, runtime_option)
            # Obtain overall results
            print(response.body)
        except Exception as error:
            # Obtain overall error information
            print(error)

    # Retrieve user information through facial ID
    def search_face_user(self, face_id):   
        try:
            user_id = Users.get_user_id_by_face_id(face_id)
            return user_id
        except Exception as error:
            # Obtain overall error information
            print("search_face_user error",error)

    # Verify the authenticity of the source of the face
    def check_face_image(self, face_base64: str):
        # Initialize client
        client = Client(self.config)
        # Build result check request
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
