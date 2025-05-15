import os
from openai import OpenAI
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
import json
import requests

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
            
            for chunk in completion:
                # 符合 SSE 格式要求
                json_dict = json.loads(chunk.model_dump_json())
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
        "model":param.model,
        "messages":param.messages,
        "stream":False,
        "enable_thinking": param.enable_thinking
    }
    if param.stream:
        def event_generator():
            # 确保使用异步客户端
            response = requests.post(apiurl, headers=headers, json=jsonable_encoder(data))
            
            for chunk in response:
                # 符合 SSE 格式要求
                json_dict = json.loads(chunk.model_dump_json())
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

            yield f"data: [DONE]\n\n" 

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        response = requests.post(apiurl, headers=headers, json=jsonable_encoder(data))
        return response.json()