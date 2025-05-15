from pydantic import BaseModel
from typing import List

class AliQwenMessageModel(BaseModel):
    role: str
    content: str

class AliQwenModelReq(BaseModel):
    model: str
    messages: List[AliQwenMessageModel]
    project: str
    stream : bool
    enable_thinking: bool

