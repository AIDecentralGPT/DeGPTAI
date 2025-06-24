import os
from apps.web.models.aimodel import AiModelReq
from anthropic import Anthropic, APIError

apikey = os.getenv("CLAUDE_API_KEY")
client = Anthropic(api_key=apikey)

class ClaudeApi:
    def check_model(self, model: str):
        models = ["claude-opus-4-20250514","claude-opus-4-20250514-think","claude-opus-4-20250514"]
        return model in models
    
    def completion(self, param: AiModelReq):
        try:
            if param.enable_thinking:
                completion = client.messages.create(
                    model=param.model,
                    messages=param.messages,
                    thinking={
                        "type": "enabled",
                        "budget_tokens": 6000
                    },
                    max_tokens=16000,
                    stream=param.stream,  #流模式
                )
            else:
                completion = client.messages.create(
                    model=param.model,
                    messages=param.messages,
                    max_tokens=10000,
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