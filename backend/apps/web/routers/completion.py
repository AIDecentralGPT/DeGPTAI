from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import json
import uuid

from fastapi import Depends
from utils.utils import (get_current_user)


from apps.web.models.aimodel import AiModelReq, AudioModelReq
from apps.web.ai.aliqwen import AliQwenApiInstance
from apps.web.ai.openai import OpenAiApiInstance
from apps.web.ai.gemini import GeminiApiInstance
from apps.web.ai.claude import ClaudeApiInstance
from apps.web.ai.deepseek import DeepseekApiInstance
from apps.web.ai.doubao import DoubaoApiInstance
from apps.web.ai.grok import GrokApiInstance


router = APIRouter()

@router.post("/completion/proxy")
async def completion_proxy(param: AiModelReq, user=Depends(get_current_user)):
    if param.audio:
        def event_generator():
            completion = OpenAiApiInstance.completionAudio(param)
            # if completion is not None:
            #     for chunk in completion:
            #         try:
            #             if chunk:
            #                 json_dict = json.loads(chunk.model_dump_json())
            #                 choice = json_dict["choices"][0]
            #                 content = choice.get("delta").get("audio").get("transcript")
            #                 if content is not None:
            #                     chat_result = {
            #                         "id": json_dict.get("id"),
            #                         "object": json_dict.get("object"),
            #                         "created": datetime.now().timestamp(),
            #                         "model": json_dict.get("model"),
            #                         "choices": [{
            #                             "index": 0,
            #                             "delta": {"content": content},
            #                             "logprobs": None,
            #                             "finish_reason": None
            #                         }]
            #                     }
            #                     yield f"data: {json.dumps(chat_result)}\n\n"
            #                 audio = choice.get("delta").get("audio").get("data")
            #                 if audio is not None:
            #                     chat_result = {
            #                         "id": json_dict.get("id"),
            #                         "object": json_dict.get("object"),
            #                         "created": datetime.now().timestamp(),
            #                         "model": json_dict.get("model"),
            #                         "choices": [{
            #                             "index": 0,
            #                             "delta": {"audio": audio},
            #                             "logprobs": None,
            #                             "finish_reason": None
            #                         }]
            #                     }
            #                     yield f"data: {json.dumps(chat_result)}\n\n"
                                
            #         except Exception as e:
            #             print("=====解析失败====", e, chunk)
            # yield f"data: [DONE]\n\n"
            if completion is not None:
                for chunk in completion:
                    json_dict = json.loads(chunk.model_dump_json())
                    try:
                        if json_dict["choices"] is not None:
                            choice = json_dict["choices"][0]
                            chat_result = {
                                "id": json_dict["id"],
                                "object": json_dict["object"],
                                "created": json_dict["created"],
                                "model": json_dict["model"],
                                "choices": [{
                                    "index": choice.get("index"),
                                    "delta": {"content": choice.get("delta").get("content")},
                                    "logprobs": choice.get("logprobs"),
                                    "finish_reason": choice.get("finish_reason")
                                }]
                            }
                            yield f"data: {json.dumps(chat_result)}\n\n"
                    except Exception as e:
                        print("=====解析失败====", chunk, e)
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
        if param.stream:
            def event_generator():
                if ClaudeApiInstance.check_model(param.model):
                    completion = ClaudeApiInstance.completion(param)
                    if completion is not None:
                        for chunk in completion:
                            try:
                                if chunk:
                                    json_dict = json.loads(chunk.model_dump_json())
                                    if json_dict.get("delta"):
                                        data = json_dict.get("delta")
                                        if data.get("thinking"):
                                            chat_result = {
                                                "id": str(uuid.uuid4()),
                                                "object": param.model,
                                                "created": datetime.now().timestamp(),
                                                "model": param.model,
                                                "choices": [{
                                                    "index": 0,
                                                    "delta": {"reasoning_content": data.get("thinking")},
                                                    "logprobs": None,
                                                    "finish_reason": None
                                                }]
                                            }
                                            yield f"data: {json.dumps(chat_result)}\n\n"
                                        if data.get("text"):
                                            chat_result = {
                                                "id": str(uuid.uuid4()),
                                                "object": param.model,
                                                "created": datetime.now().timestamp(),
                                                "model": param.model,
                                                "choices": [{
                                                    "index": 0,
                                                    "delta": {"content": data.get("text")},
                                                    "logprobs": None,
                                                    "finish_reason": None
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
                elif OpenAiApiInstance.check_model(param.model):
                    completion = OpenAiApiInstance.completion(param)
                    if completion is not None:
                        for chunk in completion:
                            try:
                                if chunk:
                                    json_dict = json.loads(chunk.model_dump_json())
                                    if json_dict.get("type") == "response.reasoning_summary_text.delta":
                                        chat_result = {
                                            "id": json_dict.get("item_id"),
                                            "object": param.model,
                                            "created": datetime.now().timestamp(),
                                            "model": param.model,
                                            "choices": [{
                                                "index": 0,
                                                "delta": {"reasoning_content": json_dict.get("delta")},
                                                "logprobs": None,
                                                "finish_reason": None
                                            }]
                                        }
                                        yield f"data: {json.dumps(chat_result)}\n\n"
                                    if json_dict.get("type") == "response.output_text.delta":
                                        chat_result = {
                                            "id": json_dict.get("item_id"),
                                            "object": param.model,
                                            "created": datetime.now().timestamp(),
                                            "model": param.model,
                                            "choices": [{
                                                "index": 0,
                                                "delta": {"content": json_dict.get("delta")},
                                                "logprobs": None,
                                                "finish_reason": None
                                            }]
                                        }
                                        yield f"data: {json.dumps(chat_result)}\n\n"
                            except Exception as e:
                                print("=====解析失败====", e, chunk)
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
                else:
                    completion = None
                    if AliQwenApiInstance.check_model(param.model):
                        completion = AliQwenApiInstance.completion(param)
                    elif GeminiApiInstance.check_model(param.model):
                        completion = GeminiApiInstance.completion(param)
                    elif DeepseekApiInstance.check_model(param.model):
                        completion = DeepseekApiInstance.completion(param)
                    elif DoubaoApiInstance.check_model(param.model):
                        completion = DoubaoApiInstance.completion(param)
                    elif GrokApiInstance.check_model(param.model):
                        completion = GrokApiInstance.completion(param)
                    
                    if completion is not None:
                        for chunk in completion:
                            try:
                                # 符合 SSE 格式要求
                                if chunk:
                                    json_dict = json.loads(chunk.model_dump_json())
                                        
                                    # 重组返回数据格式
                                    if json_dict["choices"] is not None:
                                        choice = json_dict["choices"][0]
                                        if param.enable_thinking and choice.get("delta").get("reasoning_content") is not None:
                                            chat_result = {
                                                "id": json_dict["id"],
                                                "object": json_dict["object"],
                                                "created": json_dict["created"],
                                                "model": json_dict["model"],
                                                "choices": [{
                                                    "index": choice.get("index"),
                                                    "delta": {"reasoning_content": choice.get("delta").get("reasoning_content")},
                                                    "logprobs": choice.get("logprobs"),
                                                    "finish_reason": choice.get("finish_reason")
                                                }]
                                            }
                                        else:
                                            chat_result = {
                                                "id": json_dict["id"],
                                                "object": json_dict["object"],
                                                "created": json_dict["created"],
                                                "model": json_dict["model"],
                                                "choices": [{
                                                    "index": choice.get("index"),
                                                    "delta": {"content": choice.get("delta").get("content")},
                                                    "logprobs": choice.get("logprobs"),
                                                    "finish_reason": choice.get("finish_reason")
                                                }]
                                            }
                                        yield f"data: {json.dumps(chat_result)}\n\n"
                            except Exception as e:
                                print("=====解析失败====", chunk, e)
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
            if AliQwenApiInstance.check_model(param.model):
                completion = AliQwenApiInstance.completion(param)
            elif GeminiApiInstance.check_model(param.model):
                completion = GeminiApiInstance.completion(param)
            return completion
        

@router.post("/audiototext")
async def completion_proxy(param: AudioModelReq, user=Depends(get_current_user)):
    content = AliQwenApiInstance.audioToTxt(param.data)
    return content