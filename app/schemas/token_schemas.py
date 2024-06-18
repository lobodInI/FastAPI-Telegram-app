from pydantic import BaseModel


class BaseToken(BaseModel):
    access_token: str
    token_type: str
