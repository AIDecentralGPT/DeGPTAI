import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel

apiurl = "https://api.deepseek.com"
apiurlbate = "https://api.deepseek.com/beta"
apiurlspeciale="https://api.deepseek.com/v3.2_speciale_expires_on_20251215"
apikey = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

clientbate = OpenAI(
    api_key=apikey,
    base_url=apiurlbate,
)

clientspeciale = OpenAI(
    api_key=apikey,
    base_url=apiurlspeciale,
)


class DeepseekApi:
    def check_model(self, model: str):
        models = ["deepseek-chat", "deepseek-reasoner"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            if param.enable_thinking:
                completion = clientspeciale.chat.completions.create(
                    model=param.model,
                    messages=param.messages,
                    stream=param.stream,  #流模式
                )
            else:
                if param.reload:
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