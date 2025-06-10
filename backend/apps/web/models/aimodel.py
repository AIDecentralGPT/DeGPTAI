from pydantic import BaseModel
from typing import List

class AiMessageModel(BaseModel):
    role: str
    content: str

class AiModelReq(BaseModel):
    model: str
    messages: List[AiMessageModel]
    project: str
    stream : bool
    enable_thinking: bool

