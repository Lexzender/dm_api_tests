from pydantic import (
    BaseModel,
    Field
)


class ChangePassword(BaseModel):
    login:str
    token:str
    old_password:str = Field(...,alias="oldPassword")
    new_password:str = Field(...,alias="newPassword")