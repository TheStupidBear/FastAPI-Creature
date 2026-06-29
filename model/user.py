from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    hashed_password: str
    is_superuser: int = Field(default=0)

#БД с токеном
class Token(BaseModel):
    username: str
    access_token: str
    token_type: str




