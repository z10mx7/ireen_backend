from pydantic import BaseModel
from typing import List, Optional


class SignUp(BaseModel):
    username: str
    password: str
    repassword: str
    full_name: str
    birthday: str
    email: str
    gender: Optional[str]

class Me(BaseModel):
    email: Optional[str]

class SignIn(BaseModel):
    username: str
    password: str

class CreateListing(BaseModel):
    ttype: str
    availableNow: Optional[bool]
    address: dict


