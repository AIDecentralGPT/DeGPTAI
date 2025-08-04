import os
import requests
from apps.web.models.aimodel import AiModelReq
from fastapi.encoders import jsonable_encoder
from apps.web.util.fileutils import FileUtils

apiurl = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
apikey = os.getenv("DOUBAO_API_KEY")


class DoubaoApi:
    def check_model(self, model: str):
        models = ["doubao-seed-1-6-250615", "doubao-seed-1-6-thinking-250615"]
        return model in models
   
    def completion(self, param: AiModelReq):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apikey}"
        }
        for message in param.messages:
            if isinstance(message.content, list):
                for file in message.content:
                    if file["type"] == "file":
                        file_url = file["file"]["file_data"]
                        file["file"]["file_data"] = FileUtils.url_to_data_url(file_url)
        data = {
            "model": param.model,  # 假设的模型名称，请替换为实际模型名称
            "messages": param.messages,
            "temperature": 0.7,
            "stream": True  # 启用流式输出
        }
        try:
            response = requests.post(apiurl, headers=headers, json=jsonable_encoder(data), stream=True)
            response.raise_for_status() # 非200走异常
            return response.iter_lines()
        except requests.exceptions.HTTPError as e:
            print("==========DoubaoApi Error===========", e)
            return None
        except Exception as e:
            print("==========DoubaoApi Error===========", e)
            return None
   
DoubaoApiInstance = DoubaoApi()