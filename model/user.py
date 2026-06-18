from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str
    is_superuser: int = Field(default=0)

class Token(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str





