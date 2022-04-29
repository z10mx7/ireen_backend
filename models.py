import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userName: str = Field(...)
    email: EmailStr = Field(...)
    hashedPassword: str = Field(...)
    DoB: Optional[ str ]# input year 1940 "datetime"
    gender: Optional[ str ]# input year 1940 "datetime"
    fullName: Optional[str]
    createdAt = datetime.datetime.now()
    updatedAt = datetime.datetime.now()


class Listing(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str = Field(...)
    availableNow: bool = Field(...)
    ownerId: int = Field(...)
    address: str = Field(...)
    # address: {
	# 	"streetName":  string | required
	# 	"streetNumber": string | required
	# 	"district": string | required
	# 	"city": string | required
	# }
    createdAt = datetime.datetime.now()
    updatedAt = datetime.datetime.now()

