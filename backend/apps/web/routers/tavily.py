from fastapi import APIRouter
from fastapi import Depends
from utils.utils import get_verified_user
from apps.web.models.tavily import TavilyClientInstance, TavilySearchForm


router = APIRouter()

@router.post("/search", response_model=dict)
async def search(form: TavilySearchForm):
    print("==============================", form.keywords)
    response = TavilyClientInstance.search(form.keywords)
    return response