from pydantic import BaseModel


class ChangeEmail(BaseModel):
    login: str
    password: str
    email: str