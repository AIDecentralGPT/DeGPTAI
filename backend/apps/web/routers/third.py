from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm
<<<<<<< HEAD
from concurrent.futures import ThreadPoolExecutor
=======
from apps.web.api.bing import BingApiInstance
from apps.web.api.webapi import WebApiInstance, WebInfoForm

from utils.utils import (get_current_user)
>>>>>>> fingerprintAuth-out


router = APIRouter()


@router.post("/search", response_model=dict)
<<<<<<< HEAD
async def tavilySearch(form: TavilySearchForm):
=======
async def tavilySearch(form: TavilySearchForm, user=Depends(get_current_user)):
>>>>>>> fingerprintAuth-out
    if form.type == 'twitter':
        data = TwitterApi.search_social(form.keyword)
        return { "ok": True, "data": data}
    elif form.type == 'youtube':
        data = YoutubeClientApi.search(form.keyword)
        return { "ok": True, "data": data}
<<<<<<< HEAD
    else:
        data = TavilyClientApi.search(form.keyword)
        return { "ok": True, "data": data}


@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    data = TavilyClientApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="No information obtained")
    else:
        return { "ok": True, "data": data }
    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="No information obtained")
    else:
        return { "ok": True, "data": data }
    
@router.post("/social/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search_social(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="No information obtained")
    else:
        return { "ok": True, "data": data }

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    videos = YoutubeClientApi.search(form.keyword)
    if videos is None:
        raise HTTPException(status_code=500, detail="No information obtained")
    else:
        return { "ok": True, "data": videos }
=======
    elif form.type == 'bing':
        data = BingApiInstance.bcsearch(form.keyword)
        return { "ok": True, "data": data}
    else:
        data = TavilyClientApi.search(form.keyword)
        return { "ok": True, "data": data}
    
# 校验网页数据获取
@router.post("/check_web", response_model=dict)
async def check_web(webinfo: WebInfoForm, user=Depends(get_current_user)):
    data = await WebApiInstance.getWebGraph(webinfo.url)
    return { "ok": True, "data": data}
>>>>>>> fingerprintAuth-out
