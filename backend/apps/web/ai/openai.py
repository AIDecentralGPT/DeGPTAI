import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

sysmessage = [AiMessageModel(role="system", content="You are ChatGPT, a helpful, honest, and polite AI assistant developed by OpenAI. You answer questions clearly, provide explanations when needed, and are always respectful and concise. If you are unsure about something, you say so. You aim to be as useful as possible without pretending to know things you don’t.")]

class OpenAiApi:
    def check_model(self, model: str):
        models = ["gpt-4o-mini","gpt-4o","o3","o4-mini","gpt-4.1","gpt-4.5-preview"]
        return model in models
   
    def completion(self, param: AiModelReq):
        messages = sysmessage + param.messages
        print("====================", messages)
        try:
            if param.enable_thinking:
                completion = client.chat.completions.create(
                    model=param.model,
                    reasoning_effort="medium",
                    messages=messages,
                    stream=param.stream
                )
            else:
                completion = client.chat.completions.create(
                    model=param.model,
                    messages=messages,
                    stream=param.stream,
                    temperature=0.7
                )
            
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
   
OpenAiApiInstance = OpenAiApi()