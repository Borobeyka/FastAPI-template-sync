from pydantic import BaseModel, Field


class UserAdd(BaseModel):
    username: str = Field(description="Логин")
    password: str = Field(description="Пароль")
