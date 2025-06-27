import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apiurl = "https://api.deepseek.com"
apikey = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)


class DeepseekApi:
    def check_model(self, model: str):
        models = ["deepseek-chat", "deepseek-reasoner"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  #流模式
            )
        except APIError as e:
            print("==========DeepseekApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========DeepseekApi Error===========", e)
            completion = None
        return completion
   
DeepseekApiInstance = DeepseekApi()