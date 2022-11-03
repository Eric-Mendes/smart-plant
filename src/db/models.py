from pydantic import BaseModel
from typing import List, Optional

class Info(BaseModel):
    type: str
    upper_limit: Optional[float] = False
    bottom_limit: Optional[float] = False
    
class SensorPatch(BaseModel):
    located_at: Optional[str] = False
    info: Optional[List[Info]] = False