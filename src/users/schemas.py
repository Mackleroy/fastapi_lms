from typing import Optional

from pydantic import BaseModel


class UserList(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: Optional[int]

    class Config:
        from_attributes = True
