from pydantic import BaseModel

class McpParamReq(BaseModel):
  address: str