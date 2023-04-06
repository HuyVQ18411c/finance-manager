from typing import Optional

from pydantic import BaseModel


class UserDto(BaseModel):
    user_code: Optional[str] = ''
    email: Optional[str] = ''
    password: Optional[str] = ''


class CreateUserDto(BaseModel):
    email: Optional[str] = ''
    password: Optional[str] = ''
