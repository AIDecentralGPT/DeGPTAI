import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq, AiMessageModel
from apps.web.util.fileutils import FileUtils
import base64

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
        models = ["gpt-4o-mini","gpt-4o","gpt-4o-audio-preview","o3","o4-mini","gpt-4.1", "gpt-5-mini", "gpt-5-chat-latest", "gpt-5"]
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
                        "effort": "high",       # 深度推理
                        "summary": "detailed"   # 输出详细推理步骤
                    },
                    input=param.messages,
                    stream=param.stream,
                    top_p=1,
                    tools=tools
                )
            else:
                if param.model == 'gpt-5-chat-latest':
                    completion = client.responses.create(
                        model=param.model,
                        input=param.messages,
                        stream=param.stream,
                        top_p=1
                    )
                else:
                    completion = client.responses.create(
                        model=param.model,
                        input=param.messages,
                        stream=param.stream,
                        tools=tools,
                        top_p=1
                    )         
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
    
    def completionAudio(self, param: AiModelReq):
        for message in param.messages:
            if isinstance(message.content, list):
                for file in message.content:
                    if file["type"] == "audio":
                        file["type"] = "input_audio"
                        file["input_audio"] = file["audio"]
                        del file["audio"]
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-audio-preview",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "pcm16"},
                messages= param.messages,
                stream=param.stream
            )
        except APIError as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========OpenAiApi Error===========", e)
            completion = None
        return completion
   
    def base64_to_audio(self, base64_str, output_file_path):
        """
        将Base64编码字符串转换为音频文件
        
        参数:
            base64_str: 音频的Base64编码字符串
            output_file_path: 输出音频文件的路径（需包含正确扩展名，如.mp3、.wav）
        
        返回:
            bool: 转换成功返回True，失败返回False
        """
        if not base64_str:
            print("错误：Base64字符串不能为空")
            return False
        
        try:
            # 1. 解码Base64字符串为二进制数据
            audio_bytes = base64.b64decode("data:audio/wav;base64," + base64_str)
            
            # 2. 创建输出目录（如果不存在）
            output_dir = os.path.dirname(output_file_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # 3. 将二进制数据写入音频文件
            with open(output_file_path, 'wb') as f:
                f.write(audio_bytes)
            
            print(f"音频文件已成功保存至：{output_file_path}")
            return True
        
        except base64.binascii.Error as e:
            print(f"错误：无效的Base64编码 - {str(e)}")
            return False
        except IOError as e:
            print(f"错误：文件写入失败 - {str(e)}")
            return False
        except Exception as e:
            print(f"转换过程出错：{str(e)}")
            return False

    def audio_to_base64(self, audio_file_path):
        """
        将本地语音文件转换为Base64编码字符串
        
        参数:
            audio_file_path: 语音文件的本地路径
            
        返回:
            成功时返回Base64编码字符串，失败时返回None
        """
        # 检查文件是否存在
        if not os.path.exists(audio_file_path):
            print(f"错误: 语音文件 '{audio_file_path}' 不存在")
            return None
        
        # 检查文件是否为常见的音频格式
        valid_extensions = ['.wav', '.mp3', '.aac', '.flac', '.ogg', '.m4a']
        file_ext = os.path.splitext(audio_file_path)[1].lower()
        if file_ext not in valid_extensions:
            print(f"警告: 不是常见的音频格式 ({', '.join(valid_extensions)})")
        
        try:
            # 以二进制模式读取语音文件
            with open(audio_file_path, 'rb') as audio_file:
                # 读取文件内容
                audio_data = audio_file.read()
                # 转换为Base64编码
                base64_str = base64.b64encode(audio_data).decode('utf-8')
                print(f"语音文件转换成功，大小: {len(audio_data)} 字节")
                return base64_str
        except PermissionError:
            print(f"错误: 没有权限读取文件 '{audio_file_path}'")
        except IOError as e:
            print(f"错误: 读取文件时发生IO错误 - {str(e)}")
        except Exception as e:
            print(f"错误: 转换过程中发生意外错误 - {str(e)}")
        return None

    def str_to_txt(self, base64Str, filePath):
        # 尝试打开一个不存在的文件并写入
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(base64Str)

OpenAiApiInstance = OpenAiApi()