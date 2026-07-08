from pydantic import BaseModel


class ResetPassword(BaseModel):
    login:str
    email:str