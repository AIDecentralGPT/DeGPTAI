import os
from openai import OpenAI
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
import json
import requests
import uuid
from datetime import datetime

from fastapi import Depends
from utils.utils import (get_current_user)


from apps.web.models.aliqwen import AliQwenModelReq

apiurl = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
apikey = os.getenv("DASHSCOPE_API_KEY")
client = OpenAI(
    api_key=apikey,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

router = APIRouter()

@router.post("/completion/proxy")
async def completion_proxy(param: AliQwenModelReq, user=Depends(get_current_user)):
    if param.stream:
        def event_generator():
            # 确保使用异步客户端
            completion = client.chat.completions.create(
                model=param.model,
                messages=param.messages,
                stream=True,  # 强制开启流模式
                extra_body={"enable_thinking": param.enable_thinking}
            )
            if completion is not None:
                for chunk in completion:
                    try:
                        # 符合 SSE 格式要求
                        if chunk:
                            json_dict = json.loads(chunk.model_dump_json())
                            # 重组返回数据格式
                            if json_dict["choices"] is not None:
                                if param.enable_thinking and json_dict["choices"][0]["delta"]["reasoning_content"] is not None:
                                    chat_result = {
                                        "id": json_dict["id"],
                                        "object": json_dict["object"],
                                        "created": json_dict["created"],
                                        "model": json_dict["model"],
                                        "choices": [{
                                            "index": json_dict["choices"][0]["index"],
                                            "delta": {"reasoning_content": json_dict["choices"][0]["delta"]["reasoning_content"]},
                                            "logprobs": json_dict["choices"][0]["logprobs"],
                                            "finish_reason": json_dict["choices"][0]["finish_reason"]
                                        }]
                                    }
                                else:
                                    chat_result = {
                                        "id": json_dict["id"],
                                        "object": json_dict["object"],
                                        "created": json_dict["created"],
                                        "model": json_dict["model"],
                                        "choices": [{
                                            "index": json_dict["choices"][0]["index"],
                                            "delta": {"content": json_dict["choices"][0]["delta"]["content"]},
                                            "logprobs": json_dict["choices"][0]["logprobs"],
                                            "finish_reason": json_dict["choices"][0]["finish_reason"]
                                        }]
                                    }
                                yield f"data: {json.dumps(chat_result)}\n\n"
                    except:
                        print("=====解析失败====", chunk)
            else:
                chat_result = {
                    "id": str(uuid.uuid4()),
                    "object": param.model,
                    "created": datetime.now().timestamp(),
                    "model": param.model,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": "Sorry, you don't have sufficient access rights at the moment."},
                        "logprobs": None,
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(chat_result)}\n\n"

            yield f"data: [DONE]\n\n" 

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        # 确保使用异步客户端
        completion = client.chat.completions.create(
            model=param.model,
            messages=param.messages,
            stream=False,
            extra_body={"enable_thinking": param.enable_thinking}
        )
        return completion
    
@router.post("/completion/proxy2")
async def completion_proxy2(param: AliQwenModelReq, user=Depends(get_current_user)):
    # 请求头
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }
    data = {
        "model": param.model,
        "messages": param.messages,
        "stream": param.stream,
        "enable_thinking": param.enable_thinking
    }
    if param.stream:
        def event_generator():
            # 确保使用异步客户端
            response = requests.post(apiurl, headers=headers, json=jsonable_encoder(data), stream=True)
            
            for line in response.iter_lines():
                if line:
                    # 解码字节数据并移除 data: 前缀
                    decoded_line = line.decode('utf-8').lstrip('data: ')
                    try: 
                        json_dict = json.loads(decoded_line)
                        # 符合 SSE 格式要求
                        if param.enable_thinking and json_dict["choices"][0]["delta"]["reasoning_content"] is not None:
                            chat_result = {
                                "id": json_dict["id"],
                                "object": json_dict["object"],
                                "created": json_dict["created"],
                                "model": json_dict["model"],
                                "choices": [{
                                    "index": json_dict["choices"][0]["index"],
                                    "delta": {"reasoning_content": json_dict["choices"][0]["delta"]["reasoning_content"]},
                                    "logprobs": json_dict["choices"][0]["logprobs"],
                                    "finish_reason": json_dict["choices"][0]["finish_reason"]
                                }]
                            }
                        else:
                            chat_result = {
                                "id": json_dict["id"],
                                "object": json_dict["object"],
                                "created": json_dict["created"],
                                "model": json_dict["model"],
                                "choices": [{
                                    "index": json_dict["choices"][0]["index"],
                                    "delta": {"content": json_dict["choices"][0]["delta"]["content"]},
                                    "logprobs": json_dict["choices"][0]["logprobs"],
                                    "finish_reason": json_dict["choices"][0]["finish_reason"]
                                }]
                            }
                        yield f"data: {json.dumps(chat_result)}\n\n"
                    except:
                        print(f"解析失败的行: {decoded_line}")

            yield f"data: [DONE]\n\n" 

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        response = requests.post(apiurl, headers=headers, json=jsonable_encoder(data))
        return response.json()