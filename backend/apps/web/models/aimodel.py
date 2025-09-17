from pydantic import BaseModel, Field
from typing import List, Optional

class AiMessageModel(BaseModel):
    role: str
    content: object
    prefix: Optional[bool] = Field(None, description="prefix flag") # deepseek续写字段
    partial: Optional[bool] = Field(None, description="partial flag") # aliqwen续写字段

class AiModelReq(BaseModel):
    model: str
    messages: List[AiMessageModel]
    project: str
    stream : bool
    enable_thinking: bool
    reload: bool
    audio: bool

