from fastapi import (
    FastAPI,
    Request,
    Response,
    HTTPException,
    Depends,
    status,
    UploadFile,
    File,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool

from pydantic import BaseModel, ConfigDict

import os
import re
import copy
import random
import requests
import json
import uuid
import aiohttp
import asyncio
import logging
import time
from urllib.parse import urlparse
from typing import Optional, List, Union


# from apps.web.models.users import Users
from constants import ERROR_MESSAGES
from utils.utils import (
    decode_token,
    get_current_user,
    get_verified_user,
    get_admin_user,
)


from config import (
    SRC_LOG_LEVELS,
    OLLAMA_BASE_URLS,
    ENABLE_MODEL_FILTER,
    MODEL_FILTER_LIST,
    UPLOAD_DIR,
    AppConfig,
)
from utils.misc import calculate_sha256

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OLLAMA"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.config = AppConfig()

app.state.config.ENABLE_MODEL_FILTER = ENABLE_MODEL_FILTER
app.state.config.MODEL_FILTER_LIST = MODEL_FILTER_LIST

app.state.config.OLLAMA_BASE_URLS = OLLAMA_BASE_URLS
app.state.MODELS = {}


REQUEST_POOL = []


# TODO: Implement a more intelligent load balancing mechanism for distributing requests among multiple backend instances.
# Current implementation uses a simple round-robin approach (random.choice). Consider incorporating algorithms like weighted round-robin,
# least connections, or least response time for better resource utilization and performance optimization.


@app.middleware("http")
async def check_url(request: Request, call_next):
    if len(app.state.MODELS) == 0:
        await get_all_models()
    else:
        pass

    response = await call_next(request)
    return response


@app.head("/")
@app.get("/")
async def get_status():
    return {"status": True}


@app.get("/urls")
async def get_ollama_api_urls(user=Depends(get_admin_user)):
    return {"OLLAMA_BASE_URLS": app.state.config.OLLAMA_BASE_URLS}


class UrlUpdateForm(BaseModel):
    urls: List[str]


@app.post("/urls/update")
async def update_ollama_api_url(form_data: UrlUpdateForm, user=Depends(get_admin_user)):
    app.state.config.OLLAMA_BASE_URLS = form_data.urls

    log.info(f"app.state.config.OLLAMA_BASE_URLS: {app.state.config.OLLAMA_BASE_URLS}")
    return {"OLLAMA_BASE_URLS": app.state.config.OLLAMA_BASE_URLS}


@app.get("/cancel/{request_id}")
async def cancel_ollama_request(request_id: str, user=Depends(get_current_user)):
    if user:
        if request_id in REQUEST_POOL:
            REQUEST_POOL.remove(request_id)
        return True
    else:
        raise HTTPException(status_code=401, detail=ERROR_MESSAGES.ACCESS_PROHIBITED)


async def fetch_url(url):
    timeout = aiohttp.ClientTimeout(total=5)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                return await response.json()
    except Exception as e:
        # Handle connection error here
        log.error(f"Connection error: {e}")
        return None


def merge_models_lists(model_lists):
    merged_models = {}

    for idx, model_list in enumerate(model_lists):
        if model_list is not None:
            for model in model_list:
                digest = model["digest"]
                if digest not in merged_models:
                    model["urls"] = [idx]
                    merged_models[digest] = model
                else:
                    merged_models[digest]["urls"].append(idx)

    return list(merged_models.values())


# user=Depends(get_current_user)


async def get_all_models():
    log.info("get_all_models()")
    tasks = [fetch_url(f"{url}/api/tags") for url in app.state.config.OLLAMA_BASE_URLS]
    responses = await asyncio.gather(*tasks)

    models = {
        "models": merge_models_lists(
            map(lambda response: response["models"] if response else None, responses)
        )
    }

    app.state.MODELS = {model["model"]: model for model in models["models"]}

    return models


@app.get("/api/tags")
@app.get("/api/tags/{url_idx}")
async def get_ollama_tags(
    url_idx: Optional[int] = None, user=Depends(get_verified_user)
):
    if url_idx == None:
        models = await get_all_models()

        if app.state.config.ENABLE_MODEL_FILTER:
            if user.role == "user":
                models["models"] = list(
                    filter(
                        lambda model: model["name"]
                        in app.state.config.MODEL_FILTER_LIST,
                        models["models"],
                    )
                )
                return models
        return models
    else:
        url = app.state.config.OLLAMA_BASE_URLS[url_idx]
        try:
            r = requests.request(method="GET", url=f"{url}/api/tags")
            r.raise_for_status()

            return r.json()
        except Exception as e:
            log.exception(e)
            error_detail = "DeGPT: Server Connection Error"
            if r is not None:
                try:
                    res = r.json()
                    if "error" in res:
                        error_detail = f"Ollama: {res['error']}"
                except:
                    error_detail = f"Ollama: {e}"

            raise HTTPException(
                status_code=r.status_code if r else 500,
                detail=error_detail,
            )


@app.get("/api/version")
@app.get("/api/version/{url_idx}")
async def get_ollama_versions(url_idx: Optional[int] = None):

    if url_idx == None:

        # returns lowest version
        tasks = [
            fetch_url(f"{url}/api/version") for url in app.state.config.OLLAMA_BASE_URLS
        ]
        responses = await asyncio.gather(*tasks)
        responses = list(filter(lambda x: x is not None, responses))

        if len(responses) > 0:
            lowest_version = min(
                responses,
                key=lambda x: tuple(
                    map(int, re.sub(r"^v|-.*", "", x["version"]).split("."))
                ),
            )

            return {"version": lowest_version["version"]}
        else:
            raise HTTPException(
                status_code=500,
                detail=ERROR_MESSAGES.OLLAMA_NOT_FOUND,
            )
    else:
        url = app.state.config.OLLAMA_BASE_URLS[url_idx]
        try:
            r = requests.request(method="GET", url=f"{url}/api/version")
            r.raise_for_status()

            return r.json()
        except Exception as e:
            log.exception(e)
            error_detail = "DeGPT: Server Connection Error"
            if r is not None:
                try:
                    res = r.json()
                    if "error" in res:
                        error_detail = f"Ollama: {res['error']}"
                except:
                    error_detail = f"Ollama: {e}"

            raise HTTPException(
                status_code=r.status_code if r else 500,
                detail=error_detail,
            )


class ModelNameForm(BaseModel):
    name: str


@app.post("/api/pull")
@app.post("/api/pull/{url_idx}")
async def pull_model(
    form_data: ModelNameForm, url_idx: int = 0, user=Depends(get_admin_user)
):
    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    r = None

    def get_request():
        nonlocal url
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    yield json.dumps({"id": request_id, "done": False}) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            log.warning("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        if request_id in REQUEST_POOL:
                            REQUEST_POOL.remove(request_id)

            r = requests.request(
                method="POST",
                url=f"{url}/api/pull",
                data=form_data.model_dump_json(exclude_none=True).encode(),
                stream=True,
            )

            r.raise_for_status()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)

    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


class PushModelForm(BaseModel):
    name: str
    insecure: Optional[bool] = None
    stream: Optional[bool] = None


@app.delete("/api/push")
@app.delete("/api/push/{url_idx}")
async def push_model(
    form_data: PushModelForm,
    url_idx: Optional[int] = None,
    user=Depends(get_admin_user),
):
    if url_idx == None:
        if form_data.name in app.state.MODELS:
            url_idx = app.state.MODELS[form_data.name]["urls"][0]
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.name),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.debug(f"url: {url}")

    r = None

    def get_request():
        nonlocal url
        nonlocal r
        try:

            def stream_content():
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk

            r = requests.request(
                method="POST",
                url=f"{url}/api/push",
                data=form_data.model_dump_json(exclude_none=True).encode(),
            )

            r.raise_for_status()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


class CreateModelForm(BaseModel):
    name: str
    modelfile: Optional[str] = None
    stream: Optional[bool] = None
    path: Optional[str] = None


@app.post("/api/create")
@app.post("/api/create/{url_idx}")
async def create_model(
    form_data: CreateModelForm, url_idx: int = 0, user=Depends(get_admin_user)
):
    log.debug(f"form_data: {form_data}")
    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    r = None

    def get_request():
        nonlocal url
        nonlocal r
        try:

            def stream_content():
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk

            r = requests.request(
                method="POST",
                url=f"{url}/api/create",
                data=form_data.model_dump_json(exclude_none=True).encode(),
                stream=True,
            )

            r.raise_for_status()

            log.debug(f"r: {r}")

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


class CopyModelForm(BaseModel):
    source: str
    destination: str


@app.post("/api/copy")
@app.post("/api/copy/{url_idx}")
async def copy_model(
    form_data: CopyModelForm,
    url_idx: Optional[int] = None,
    user=Depends(get_admin_user),
):
    if url_idx == None:
        if form_data.source in app.state.MODELS:
            url_idx = app.state.MODELS[form_data.source]["urls"][0]
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.source),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    try:
        r = requests.request(
            method="POST",
            url=f"{url}/api/copy",
            data=form_data.model_dump_json(exclude_none=True).encode(),
        )
        r.raise_for_status()

        log.debug(f"r.text: {r.text}")

        return True
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


@app.delete("/api/delete")
@app.delete("/api/delete/{url_idx}")
async def delete_model(
    form_data: ModelNameForm,
    url_idx: Optional[int] = None,
    user=Depends(get_admin_user),
):
    if url_idx == None:
        if form_data.name in app.state.MODELS:
            url_idx = app.state.MODELS[form_data.name]["urls"][0]
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.name),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    try:
        r = requests.request(
            method="DELETE",
            url=f"{url}/api/delete",
            data=form_data.model_dump_json(exclude_none=True).encode(),
        )
        r.raise_for_status()

        log.debug(f"r.text: {r.text}")

        return True
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


@app.post("/api/show")
async def show_model_info(form_data: ModelNameForm, user=Depends(get_verified_user)):
    if form_data.name not in app.state.MODELS:
        raise HTTPException(
            status_code=400,
            detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.name),
        )

    url_idx = random.choice(app.state.MODELS[form_data.name]["urls"])
    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    try:
        r = requests.request(
            method="POST",
            url=f"{url}/api/show",
            data=form_data.model_dump_json(exclude_none=True).encode(),
        )
        r.raise_for_status()

        return r.json()
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


class GenerateEmbeddingsForm(BaseModel):
    model: str
    prompt: str
    options: Optional[dict] = None
    keep_alive: Optional[Union[int, str]] = None


@app.post("/api/embeddings")
@app.post("/api/embeddings/{url_idx}")
async def generate_embeddings(
    form_data: GenerateEmbeddingsForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):
    if url_idx == None:
        model = form_data.model

        if ":" not in model:
            model = f"{model}:latest"

        if model in app.state.MODELS:
            url_idx = random.choice(app.state.MODELS[model]["urls"])
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.model),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    try:
        r = requests.request(
            method="POST",
            url=f"{url}/api/embeddings",
            data=form_data.model_dump_json(exclude_none=True).encode(),
        )
        r.raise_for_status()

        return r.json()
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


def generate_ollama_embeddings(
    form_data: GenerateEmbeddingsForm,
    url_idx: Optional[int] = None,
):

    log.info(f"generate_ollama_embeddings {form_data}")

    if url_idx == None:
        model = form_data.model

        if ":" not in model:
            model = f"{model}:latest"

        if model in app.state.MODELS:
            url_idx = random.choice(app.state.MODELS[model]["urls"])
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.model),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    try:
        r = requests.request(
            method="POST",
            url=f"{url}/api/embeddings",
            data=form_data.model_dump_json(exclude_none=True).encode(),
        )
        r.raise_for_status()

        data = r.json()

        log.info(f"generate_ollama_embeddings {data}")

        if "embedding" in data:
            return data["embedding"]
        else:
            raise "Something went wrong :/"
    except Exception as e:
        log.exception(e)
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise error_detail


class GenerateCompletionForm(BaseModel):
    model: str
    prompt: str
    images: Optional[List[str]] = None
    format: Optional[str] = None
    options: Optional[dict] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[str] = None
    stream: Optional[bool] = True
    raw: Optional[bool] = None
    keep_alive: Optional[Union[int, str]] = None


@app.post("/api/generate")
@app.post("/api/generate/{url_idx}")
async def generate_completion(
    form_data: GenerateCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):

    if url_idx == None:
        model = form_data.model

        if ":" not in model:
            model = f"{model}:latest"

        if model in app.state.MODELS:
            url_idx = random.choice(app.state.MODELS[model]["urls"])
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.model),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    r = None

    def get_request():
        nonlocal form_data
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    if form_data.stream:
                        yield json.dumps({"id": request_id, "done": False}) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            log.warning("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        if request_id in REQUEST_POOL:
                            REQUEST_POOL.remove(request_id)

            r = requests.request(
                method="POST",
                url=f"{url}/api/generate",
                data=form_data.model_dump_json(exclude_none=True).encode(),
                stream=True,
            )

            r.raise_for_status()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


class ChatMessage(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None


class GenerateChatCompletionForm(BaseModel):
    model: str
    messages: List[ChatMessage]
    format: Optional[str] = None
    options: Optional[dict] = None
    template: Optional[str] = None
    stream: Optional[bool] = None
    keep_alive: Optional[Union[int, str]] = None


@app.post("/api/chat")
@app.post("/api/chat/{url_idx}")
async def generate_chat_completion(
    form_data: GenerateChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):

    if url_idx == None:
        model = form_data.model

        if ":" not in model:
            model = f"{model}:latest"

        if model in app.state.MODELS:
            url_idx = random.choice(app.state.MODELS[model]["urls"])
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.model),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    r = None

    log.debug(
        "form_data.model_dump_json(exclude_none=True).encode(): {0} ".format(
            form_data.model_dump_json(exclude_none=True).encode()
        )
    )

    def get_request():
        nonlocal form_data
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    if form_data.stream:
                        yield json.dumps({"id": request_id, "done": False}) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            log.warning("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        if request_id in REQUEST_POOL:
                            REQUEST_POOL.remove(request_id)

            r = requests.request(
                method="POST",
                url=f"{url}/api/chat",
                data=form_data.model_dump_json(exclude_none=True).encode(),
                stream=True,
            )

            r.raise_for_status()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            log.exception(e)
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


# TODO: we should update this part once Ollama supports other types
class OpenAIChatMessage(BaseModel):
    role: str
    content: str

    model_config = ConfigDict(extra="allow")


class OpenAIChatCompletionForm(BaseModel):
    model: str
    messages: List[OpenAIChatMessage]

    model_config = ConfigDict(extra="allow")





# 这是ollama！！！不要看这里！！！！！
@app.post("/v1/chat/completions")
@app.post("/v1/chat/completions/{url_idx}")
async def generate_openai_chat_completion(
    form_data: OpenAIChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):
    """
    生成OpenAI聊天补全结果
    
    Args:
        form_data (OpenAIChatCompletionForm): 聊天补全表单数据
        url_idx (Optional[int], optional): URL索引. Defaults to None.
        user (Depends): 验证用户信息. Defaults to Depends(get_verified_user).
    
    Returns:
        StreamingResponse: 聊天补全结果的流式响应
    
    Raises:
        HTTPException: 当模型不存在或服务器连接错误时抛出异常
    """

    if url_idx == None:
        model = form_data.model

        print("generate_openai_chat_completion: model", model)
        
        if ":" not in model:
            model = f"{model}:latest"

        if model in app.state.MODELS:
            url_idx = random.choice(app.state.MODELS[model]["urls"])
        else:
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES.MODEL_NOT_FOUND(form_data.model),
            )

    url = app.state.config.OLLAMA_BASE_URLS[url_idx]
    log.info(f"url: {url}")

    r = None

    def get_request():
        nonlocal form_data
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    if form_data.stream:
                        yield json.dumps(
                            {"request_id": request_id, "done": False}
                        ) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            log.warning("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        if request_id in REQUEST_POOL:
                            REQUEST_POOL.remove(request_id)

            r = requests.request(
                method="POST",
                url=f"{url}/v1/chat/completions",
                data=form_data.model_dump_json(exclude_none=True).encode(),
                stream=True,
            )

            r.raise_for_status()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )


@app.get("/v1/models")
@app.get("/v1/models/{url_idx}")
async def get_openai_models(
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):
    if url_idx == None:
        models = await get_all_models()

        if app.state.config.ENABLE_MODEL_FILTER:
            if user.role == "user":
                models["models"] = list(
                    filter(
                        lambda model: model["name"]
                        in app.state.config.MODEL_FILTER_LIST,
                        models["models"],
                    )
                )

        return {
            "data": [
                {
                    "id": model["model"],
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "openai",
                }
                for model in models["models"]
            ],
            "object": "list",
        }

    else:
        url = app.state.config.OLLAMA_BASE_URLS[url_idx]
        try:
            r = requests.request(method="GET", url=f"{url}/api/tags")
            r.raise_for_status()

            models = r.json()

            return {
                "data": [
                    {
                        "id": model["model"],
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "openai",
                    }
                    for model in models["models"]
                ],
                "object": "list",
            }

        except Exception as e:
            log.exception(e)
            error_detail = "DeGPT: Server Connection Error"
            if r is not None:
                try:
                    res = r.json()
                    if "error" in res:
                        error_detail = f"Ollama: {res['error']}"
                except:
                    error_detail = f"Ollama: {e}"

            raise HTTPException(
                status_code=r.status_code if r else 500,
                detail=error_detail,
            )


class UrlForm(BaseModel):
    url: str


class UploadBlobForm(BaseModel):
    filename: str


def parse_huggingface_url(hf_url):
    try:
        # Parse the URL
        parsed_url = urlparse(hf_url)

        # Get the path and split it into components
        path_components = parsed_url.path.split("/")

        # Extract the desired output
        user_repo = "/".join(path_components[1:3])
        model_file = path_components[-1]

        return model_file
    except ValueError:
        return None


async def download_file_stream(
    ollama_url, file_url, file_path, file_name, chunk_size=1024 * 1024
):
    done = False

    if os.path.exists(file_path):
        current_size = os.path.getsize(file_path)
    else:
        current_size = 0

    headers = {"Range": f"bytes={current_size}-"} if current_size > 0 else {}

    timeout = aiohttp.ClientTimeout(total=600)  # Set the timeout

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(file_url, headers=headers) as response:
            total_size = int(response.headers.get("content-length", 0)) + current_size

            with open(file_path, "ab+") as file:
                async for data in response.content.iter_chunked(chunk_size):
                    current_size += len(data)
                    file.write(data)

                    done = current_size == total_size
                    progress = round((current_size / total_size) * 100, 2)

                    yield f'data: {{"progress": {progress}, "completed": {current_size}, "total": {total_size}}}\n\n'

                if done:
                    file.seek(0)
                    hashed = calculate_sha256(file)
                    file.seek(0)

                    url = f"{ollama_url}/api/blobs/sha256:{hashed}"
                    response = requests.post(url, data=file)

                    if response.ok:
                        res = {
                            "done": done,
                            "blob": f"sha256:{hashed}",
                            "name": file_name,
                        }
                        os.remove(file_path)

                        yield f"data: {json.dumps(res)}\n\n"
                    else:
                        raise "Ollama: Could not create blob, Please try again."


# def number_generator():
#     for i in range(1, 101):
#         yield f"data: {i}\n"


# url = "https://huggingface.co/TheBloke/stablelm-zephyr-3b-GGUF/resolve/main/stablelm-zephyr-3b.Q2_K.gguf"
@app.post("/models/download")
@app.post("/models/download/{url_idx}")
async def download_model(
    form_data: UrlForm,
    url_idx: Optional[int] = None,
):

    allowed_hosts = ["https://huggingface.co/", "https://github.com/"]

    if not any(form_data.url.startswith(host) for host in allowed_hosts):
        raise HTTPException(
            status_code=400,
            detail="Invalid file_url. Only URLs from allowed hosts are permitted.",
        )

    if url_idx == None:
        url_idx = 0
    url = app.state.config.OLLAMA_BASE_URLS[url_idx]

    file_name = parse_huggingface_url(form_data.url)

    if file_name:
        file_path = f"{UPLOAD_DIR}/{file_name}"

        return StreamingResponse(
            download_file_stream(url, form_data.url, file_path, file_name),
        )
    else:
        return None


@app.post("/models/upload")
@app.post("/models/upload/{url_idx}")
def upload_model(file: UploadFile = File(...), url_idx: Optional[int] = None):
    if url_idx == None:
        url_idx = 0
    ollama_url = app.state.config.OLLAMA_BASE_URLS[url_idx]

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file in chunks
    with open(file_path, "wb+") as f:
        for chunk in file.file:
            f.write(chunk)

    def file_process_stream():
        nonlocal ollama_url
        total_size = os.path.getsize(file_path)
        chunk_size = 1024 * 1024
        try:
            with open(file_path, "rb") as f:
                total = 0
                done = False

                while not done:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        done = True
                        continue

                    total += len(chunk)
                    progress = round((total / total_size) * 100, 2)

                    res = {
                        "progress": progress,
                        "total": total_size,
                        "completed": total,
                    }
                    yield f"data: {json.dumps(res)}\n\n"

                if done:
                    f.seek(0)
                    hashed = calculate_sha256(f)
                    f.seek(0)

                    url = f"{ollama_url}/api/blobs/sha256:{hashed}"
                    response = requests.post(url, data=f)

                    if response.ok:
                        res = {
                            "done": done,
                            "blob": f"sha256:{hashed}",
                            "name": file.filename,
                        }
                        os.remove(file_path)
                        yield f"data: {json.dumps(res)}\n\n"
                    else:
                        raise Exception(
                            "Ollama: Could not create blob, Please try again."
                        )

        except Exception as e:
            res = {"error": str(e)}
            yield f"data: {json.dumps(res)}\n\n"

    return StreamingResponse(file_process_stream(), media_type="text/event-stream")


# async def upload_model(file: UploadFile = File(), url_idx: Optional[int] = None):
#     if url_idx == None:
#         url_idx = 0
#     url = app.state.config.OLLAMA_BASE_URLS[url_idx]

#     file_location = os.path.join(UPLOAD_DIR, file.filename)
#     total_size = file.size

#     async def file_upload_generator(file):
#         print(file)
#         try:
#             async with aiofiles.open(file_location, "wb") as f:
#                 completed_size = 0
#                 while True:
#                     chunk = await file.read(1024*1024)
#                     if not chunk:
#                         break
#                     await f.write(chunk)
#                     completed_size += len(chunk)
#                     progress = (completed_size / total_size) * 100

#                     print(progress)
#                     yield f'data: {json.dumps({"status": "uploading", "percentage": progress, "total": total_size, "completed": completed_size, "done": False})}\n'
#         except Exception as e:
#             print(e)
#             yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n"
#         finally:
#             await file.close()
#             print("done")
#             yield f'data: {json.dumps({"status": "completed", "percentage": 100, "total": total_size, "completed": completed_size, "done": True})}\n'

#     return StreamingResponse(
#         file_upload_generator(copy.deepcopy(file)), media_type="text/event-stream"
#     )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def deprecated_proxy(
    path: str, request: Request, user=Depends(get_verified_user)
):
    url = app.state.config.OLLAMA_BASE_URLS[0]
    target_url = f"{url}/{path}"

    body = await request.body()
    headers = dict(request.headers)

    if user.role in ["user", "admin"]:
        if path in ["pull", "delete", "push", "copy", "create"]:
            if user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )

    headers.pop("host", None)
    headers.pop("authorization", None)
    headers.pop("origin", None)
    headers.pop("referer", None)

    r = None

    def get_request():
        nonlocal r

        request_id = str(uuid.uuid4())
        try:
            REQUEST_POOL.append(request_id)

            def stream_content():
                try:
                    if path == "generate":
                        data = json.loads(body.decode("utf-8"))

                        if not ("stream" in data and data["stream"] == False):
                            yield json.dumps({"id": request_id, "done": False}) + "\n"

                    elif path == "chat":
                        yield json.dumps({"id": request_id, "done": False}) + "\n"

                    for chunk in r.iter_content(chunk_size=8192):
                        if request_id in REQUEST_POOL:
                            yield chunk
                        else:
                            log.warning("User: canceled request")
                            break
                finally:
                    if hasattr(r, "close"):
                        r.close()
                        if request_id in REQUEST_POOL:
                            REQUEST_POOL.remove(request_id)

            r = requests.request(
                method=request.method,
                url=target_url,
                data=body,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            # r.close()

            return StreamingResponse(
                stream_content(),
                status_code=r.status_code,
                headers=dict(r.headers),
            )
        except Exception as e:
            raise e

    try:
        return await run_in_threadpool(get_request)
    except Exception as e:
        error_detail = "DeGPT: Server Connection Error"
        if r is not None:
            try:
                res = r.json()
                if "error" in res:
                    error_detail = f"Ollama: {res['error']}"
            except:
                error_detail = f"Ollama: {e}"

        raise HTTPException(
            status_code=r.status_code if r else 500,
            detail=error_detail,
        )
