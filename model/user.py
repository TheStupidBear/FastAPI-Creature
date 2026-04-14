from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    password: str
    is_superuser: int = Field(default=0)