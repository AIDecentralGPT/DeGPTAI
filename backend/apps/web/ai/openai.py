import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)


class OpenAiApi:
    def check_model(self, model: str):
        models = ["gpt-4.1","o4-mini","o3"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  #流模式
            )
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
   
OpenAiApiInstance = OpenAiApi()