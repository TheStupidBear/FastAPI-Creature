from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str
    is_superuser: int = Field(default=0)


