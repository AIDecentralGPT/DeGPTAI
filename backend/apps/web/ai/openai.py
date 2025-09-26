import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel
from apps.web.util.fileutils import FileUtils
import base64
import requests
from io import BytesIO

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

# sysmessage = [AiMessageModel(role="system", content="You are ChatGPT, a helpful, honest, and polite AI assistant developed by OpenAI. You answer questions clearly, provide explanations when needed, and are always respectful and concise. If you are unsure about something, you say so. You aim to be as useful as possible without pretending to know things you don’t.")]
sysmessage = [AiMessageModel(role="system", content="用中文回复")]
tools = [
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Query a knowledge base to retrieve relevant info on a topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user question or search query.",
                },
                "options": {
                    "type": "object",
                    "properties": {
                        "num_results": {
                            "type": "number",
                            "description": "Number of top results to return.",
                        },
                        "domain_filter": {
                            "type": ["string", "null"],
                            "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed.",
                        },
                        "sort_by": {
                            "type": ["string", "null"],
                            "enum": ["relevance", "date", "popularity", "alphabetical"],
                            "description": "How to sort results. Pass null if not needed.",
                        },
                    },
                    "required": ["num_results", "domain_filter", "sort_by"],
                    "additionalProperties": False,
                },
            },
            "required": ["query", "options"],
            "additionalProperties": False,
        },
    }
]


class OpenAiApi:
    def check_model(self, model: str):
        models = [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4o-audio-preview",
            "o3",
            "o4-mini",
            "gpt-4.1",
            "gpt-5-mini",
            "gpt-5-chat-latest",
            "gpt-5",
        ]
        return model in models

    def completion(self, param: AiModelReq):
        for message in param.messages:
            if isinstance(message.content, list):
                for file in message.content:
                    if file["type"] == "text":
                        file["type"] = "input_text"
                    if file["type"] == "image_url":
                        file["type"] = "input_image"
                        file["image_url"] = file["image_url"]["url"]
                    if file["type"] == "file":
                        file["type"] = "input_file"
                        file_url = file["file"]["file_data"]
                        file["file_url"] = file_url
                        del file["file"]
        try:
            if param.enable_thinking:
                completion = client.responses.create(
                    model=param.model,
                    reasoning={
                        "effort": "high",  # 深度推理
                        "summary": "detailed",  # 输出详细推理步骤
                    },
                    input=param.messages,
                    stream=param.stream,
                    top_p=1,
                    tools=tools,
                )
            else:
                if param.model == "gpt-5-chat-latest":
                    completion = client.responses.create(
                        model=param.model,
                        input=param.messages,
                        stream=param.stream,
                        top_p=1,
                    )
                else:
                    completion = client.responses.create(
                        model=param.model,
                        input=param.messages,
                        stream=param.stream,
                        tools=tools,
                        top_p=1,
                    )
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion

    def completionAudio(self, param: AiModelReq):
        for message in list(param.messages):  # 遍历副本
            if isinstance(message.content, list):
                for file in message.content:
                    if file.get("type") == "audio":
                        base64Str = self.audio_url_to_base64(file["audio"]["data"])
                        if base64Str is None:
                            # 删除整个 message
                            param.messages.remove(message)  # 直接操作原始列表
                            break
                        else:
                            # 修改 file 字典（会影响原数据）
                            file["type"] = "input_audio"
                            file["audio"]["data"] = base64Str
                            file["input_audio"] = file["audio"]
                            del file["audio"]
        try:
            completion = client.chat.completions.create(
                model=param.model,
                modalities=["text"],
                audio={"voice": "alloy", "format": "pcm16"},
                messages=param.messages,
                stream=param.stream,
                stream_options={"include_usage": True},
                frequency_penalty=0,
                presence_penalty=0,
                max_completion_tokens=2048,
                temperature=1,
                top_p=1
            )
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
    

    def audioToTxt(self, audioStr: str):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-audio-preview",
                modalities=["text"],
                audio={"voice": "alloy", "format": "pcm16"},
                frequency_penalty=0,
                presence_penalty=0,
                max_completion_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_audio",
                                "input_audio": {"data": audioStr, "format": "wav"},
                            },
                            {"type": "text", "text": "You are an audio recognition result output tool and shall only return the recognized text as a string. Task: Perform audio recognition on the input audio. Requirements: 1. The content must strictly match the audio content, and unclear parts shall be marked with *. 2. Only output the recognized text without any extra characters."},
                        ]
                    }
                ],
                stream=False,
                temperature=1,
                top_p=1
            )
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion


    def audio_url_to_base64(self, audio_url):
        try:
            response = requests.get(audio_url, stream=True)
            response.raise_for_status()   
            audio_bytes = BytesIO(response.content)          
            base64_encoded = base64.b64encode(audio_bytes.read()).decode('utf-8')           
            return base64_encoded          
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        except Exception as e:
            print(f"处理错误: {e}")   
        return None

OpenAiApiInstance = OpenAiApi()
