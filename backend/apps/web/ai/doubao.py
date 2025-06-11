import os
import requests
from apps.web.models.aimodel import AiModelReq
from fastapi.encoders import jsonable_encoder

apiurl = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
apikey = os.getenv("DOUBAO_API_KEY")


class DoubaoApi:
    def check_model(self, model: str):
        models = ["doubao-1.5-vision-pro-250328"]
        return model in models
   
    def completion(self, param: AiModelReq):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apikey}"
        }
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