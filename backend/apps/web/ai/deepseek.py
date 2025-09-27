import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel

apiurl = "https://api.deepseek.com"
apiurlbate = "https://api.deepseek.com/beta"
apikey = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

clientbate = OpenAI(
    api_key=apikey,
    base_url=apiurlbate,
)


class DeepseekApi:
    def check_model(self, model: str):
        models = ["deepseek-chat", "deepseek-reasoner"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            if (param.reload):
                param.messages[-1].prefix = True
                completion = clientbate.chat.completions.create(
                    model=param.model,
                    messages=param.messages,
                    stream=param.stream,  #流模式
                    stop=["```"],
                )           
            else:
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