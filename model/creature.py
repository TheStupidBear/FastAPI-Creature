from pydantic import BaseModel
from typing import Optional

class Creature(BaseModel):
    name: str
    country: str
    area: Optional[str] = None #необязательное поле
    description: str
    aka: Optional[str] = None
    user: str