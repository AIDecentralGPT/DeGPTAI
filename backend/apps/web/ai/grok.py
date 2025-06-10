import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apiurl = "https://api.x.ai/v1"
apikey = os.getenv("GROK_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

class GrokApi:
   def check_model(self, model: str):
        models = ["grok-3", "grok-3-mini"]
        return model in models
   
   def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  # 流模式
                extra_body={"enable_thinking": param.enable_thinking}
            )
        except APIError as e:
            print("==========GrokApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========GrokApi Error===========", e)
            completion = None
        return completion
   
GrokApiInstance = GrokApi()