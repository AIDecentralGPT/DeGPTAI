from pydantic import BaseModel

class UploadBase(BaseModel):
  data: str