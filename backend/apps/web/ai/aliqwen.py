import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apiurl = "https://dashscope.aliyuncs.com/compatible-mode/v1"
apikey = os.getenv("ALIQWEN_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

class AliQwenApi:
   def check_model(self, model: str):
        models = ["qwen3-235b-a22b", "qwen-vl-plus", "qvq-max", "qwen3-max-preview"]
        return model in models
   
   def completion(self, param: AiModelReq):
        try:
            if param.reload and param.enable_thinking is False:
                param.messages[-1].partial = True
                
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  # 流模式
                extra_body={"enable_thinking": param.enable_thinking}
            )
        except APIError as e:
            print("==========AliQwenApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========AliQwenApi Error===========", e)
            completion = None
        return completion
   
AliQwenApiInstance = AliQwenApi()