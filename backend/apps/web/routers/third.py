from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm
from apps.web.api.bing import BingApiInstance
from apps.web.api.webapi import WebApiInstance, WebInfoForm
from apps.web.api.playrighttwitter import PlayWrightInstall

from utils.utils import (get_current_user)


router = APIRouter()


@router.post("/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm, user=Depends(get_current_user)):
    if form.type == 'twitter':
        data = await PlayWrightInstall.get_twitter_content(form.keyword)
        return { "ok": True, "data": data}
    elif form.type == 'youtube':
        data = YoutubeClientApi.search(form.keyword)
        return { "ok": True, "data": data}
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