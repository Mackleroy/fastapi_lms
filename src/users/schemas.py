from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str
    age: Optional[int]


class UserDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str
    age: Optional[int]
