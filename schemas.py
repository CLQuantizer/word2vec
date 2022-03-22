from typing import List, Optional
from pydantic import BaseModel


class WritingBase(BaseModel):
    title: str
    body: Optional[str] = None

class WritingCreate(WritingBase):
    pass

class Writing(WritingBase):
    id: int
    class Config:
        orm_mode = True
