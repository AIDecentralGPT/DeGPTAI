import os
import requests
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq
from fastapi.encoders import jsonable_encoder

apiurl = "https://ark.cn-beijing.volces.com/api/v3"
apikey = os.getenv("DOUBAO_API_KEY")

client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)


class DoubaoApi:
    def check_model(self, model: str):
        models = ["doubao-seed-1-6-250615", "doubao-seed-1-6-thinking-250615"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  #流模式
                extra_body={
                    "thinking": {
                        "type": "enabled" if param.enable_thinking else "disabled"
                    }
                }
            )
        except APIError as e:
            print("==========DoubaoApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========DoubaoApi Error===========", e)
            completion = None
        return completion

DoubaoApiInstance = DoubaoApi()