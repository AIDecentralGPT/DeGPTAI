from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils.utils import get_verified_user
from apps.web.api.tavily import TavilyClientApi, TavilySearchForm
from apps.web.api.youtube import YoutubeClientApi, YoutubeSearchForm
from apps.web.api.twitter import TwitterApi, TwitterSearchForm
import random
from concurrent.futures import ThreadPoolExecutor
import jieba


router = APIRouter()


@router.post("/web/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    seg_list = jieba.cut(form.keyword, cut_all=False)
    print("============分解keyword============")
    keyword = "/".join(seg_list)
    print("========================", keyword)
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务并收集 Future 对象
        futures = [executor.submit(thirdTask, i, keyword) for i in range(3)]
        # 直接通过 Future 对象获取返回值（按完成顺序）
        for future in futures:
            results.append(future.result())
    web_data = {"keyword": keyword, "websearch": [], "thumbearch": [], "content": ""}
    for result in results:
        if result["data"] is not None:
            if result["type"] == "web":
                web_data['websearch'].extend(result["data"])
                for item in result["data"]:
                    web_data['content'] = f"{web_data['content']},{item.get('content')}"
            if result["type"] == "twitter":
                web_data['thumbearch'].extend(result["data"])
                for item in result["data"]:
                    web_data['content'] = f"{web_data['content']},{item.get('title')}"
            if result.get("type") == "youtube":
                web_data['thumbearch'].extend(result["data"])
                for item in result["data"]:
                    web_data['content'] = f"{web_data['content']},{item.get('title')}"
    return { "ok": True, "data": web_data}


def thirdTask(index, keyword):
    if index == 0:
        data = TavilyClientApi.search(keyword)
        return {"type": "web", "data": data}
    if index == 1:
        data = TwitterApi.search(keyword)
        return {"type": "twitter", "data": data}
    if index == 2:
        data = YoutubeClientApi.search(keyword)
        return {"type": "youtube", "data": data}


@router.post("/tavily/search", response_model=dict)
async def tavilySearch(form: TavilySearchForm):
    data = TavilyClientApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }
    

@router.post("/video/search", response_model=dict)
async def videoSearch(form: YoutubeSearchForm):
    data = []
    twitterData = TwitterApi.search(form.keyword)
    if twitterData is not None:
        data.extend(twitterData)
    youtubeData = YoutubeClientApi.search(form.keyword)
    if youtubeData is not None:
        data.extend(youtubeData)
    # 打乱列表顺序
    random.shuffle(data)
    return { "ok": True, "data": data }

    
@router.post("/twitter/search", response_model=dict)
async def twitterSearch(form: TwitterSearchForm):
    data = TwitterApi.search(form.keyword)
    if data is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": data }

@router.post("/youtube/search", response_model=dict)
async def youtubeSearch(form: YoutubeSearchForm):
    videos = YoutubeClientApi.search(form.keyword)
    if videos is None:
        raise HTTPException(status_code=500, detail="未获取到信息")
    else:
        return { "ok": True, "data": videos }