import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

#sysmessage = [AiMessageModel(role="system", content="You are ChatGPT, a helpful, honest, and polite AI assistant developed by OpenAI. You answer questions clearly, provide explanations when needed, and are always respectful and concise. If you are unsure about something, you say so. You aim to be as useful as possible without pretending to know things you don’t.")]
sysmessage = [AiMessageModel(role="system", content="用中文回复")]
tools = [{
    "type": "function",
    "name": "search_knowledge_base",
    "description": "Query a knowledge base to retrieve relevant info on a topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The user question or search query."
            },
            "options": {
                "type": "object",
                "properties": {
                    "num_results": {
                        "type": "number",
                        "description": "Number of top results to return."
                    },
                    "domain_filter": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed."
                    },
                    "sort_by": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "enum": [
                            "relevance",
                            "date",
                            "popularity",
                            "alphabetical"
                        ],
                        "description": "How to sort results. Pass null if not needed."
                    }
                },
                "required": [
                    "num_results",
                    "domain_filter",
                    "sort_by"
                ],
                "additionalProperties": False
            }
        },
        "required": [
            "query",
            "options"
        ],
        "additionalProperties": False
    }
}]

class OpenAiApi:
    def check_model(self, model: str):
        models = ["gpt-4o-mini","gpt-4o","o3","o4-mini","gpt-4.1","gpt-4.5-preview"]
        return model in models
   
    def completion(self, param: AiModelReq):
        messages = param.messages
        try:
            if param.enable_thinking:
                completion = client.responses.create(
                    model=param.model,
                    reasoning={
                        "effort": "high",       # 深度推理
                        "summary": "detailed"   # 输出详细推理步骤
                    },
                    input=messages,
                    stream=param.stream,
                    tools=tools,
                    top_p=1,
                    store=False
                )
            else:
                completion = client.responses.create(
                    model=param.model,
                    input=messages,
                    stream=param.stream,
                    top_p=1,
                    store=False
                )
            
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
   
OpenAiApiInstance = OpenAiApi()