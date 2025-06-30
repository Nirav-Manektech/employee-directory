from typing import List, Dict, Any
from pydantic import BaseModel

class Meta(BaseModel):
    total: int
    limit: int
    offset: int

class SearchResponse(BaseModel):
    data: List[Dict[str, Any]]
    meta: Meta
