import os
from openai import OpenAI, APIError
from apps.web.models.aimodel import AiModelReq
import dashscope
from http import HTTPStatus
import json
import requests
import re

apiurl = "https://dashscope.aliyuncs.com/compatible-mode/v1"
apikey = os.getenv("ALIQWEN_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url=apiurl,
)

dashscope.api_key = apikey


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
                extra_body={"enable_thinking": param.enable_thinking},
            )
        except APIError as e:
            print("==========AliQwenApi Error===========", e)
            completion = None
        except Exception as e:
            print("==========AliQwenApi Error===========", e)
            completion = None
        return completion

    def audioToTxt(self, audioStr: str):
        outtext = []
        task_response = dashscope.audio.asr.Transcription.async_call(
            model='sensevoice-v1',
            file_urls=[audioStr],
        )
        transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
        if transcribe_response.status_code == HTTPStatus.OK:
            results = transcribe_response.output.get("results")    
            for result in results:
                resultjson = self.read_json_from_url(result.get("transcription_url"))
                outtext = self.extract_speech_text(resultjson)
        
        return {"data": ",".join(outtext)}

    def read_json_from_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            return json_data       
        except requests.exceptions.RequestException as e:
            print(f"请求错误1: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
        except Exception as e:
            print(f"发生错误2: {e}") 
        return None

    def extract_speech_text(self, data):
        pattern = r'<\|Speech\|>(.*?)<\|/Speech\|>'
        results = [] 
        for transcript in data.get('transcripts', []):
            text = transcript.get('text', '')
            matches = re.findall(pattern, text, re.DOTALL)
            results.extend([match.strip() for match in matches]) 
        return results

AliQwenApiInstance = AliQwenApi()
