import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq

apiurl = "https://api.anthropic.com/v1/"
apikey = os.getenv("CLAUDE_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)


class ClaudeApi:
    def check_model(self, model: str):
        models = ["claude-opus-4-20250514"]
        return model in models
   
    def completion(self, param: AiModelReq):
        try:
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=param.stream,  #流模式
            )
        except APIError as e:
            print("==========ClaudeApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========ClaudeApi Error===========", e)
            completion = None
        return completion
   
ClaudeApiInstance = ClaudeApi()