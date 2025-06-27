import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apiurl = "https://generativelanguage.googleapis.com/v1beta/openai/"
apikey = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

class GeminiApi:
   def check_model(self, model: str):
        models = ["gemini-2.5-flash-preview-05-20", "gemini-2.5-pro"]
        return model in models
   
   def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  #流模式
            )
        except APIError as e:
            print("==========GeminiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========GeminiApi Error===========", e)
            completion = None
        return completion
   
GeminiApiInstance = GeminiApi()