import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from beanie import Document, Indexed
from bson.objectid import ObjectId
from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field

class UserModel(Document):
    user_id: Indexed(str, unique=True) = uuid4().hex
    username: Indexed(str, unique=True)
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[str]
    educational_details: Optional[str]
    # email_address: Optional[str]
    contact_no: Optional[int]
    skills: Optional[List[str]]
    internship_details: Optional[List[str]]
    yoj: Optional[int]
    yop: Optional[int]
    department: Optional[str]
    course: Optional[str]
    current_semeseter: Optional[int]
    bio: Optional[str]
    address: Optional[str]
    hostel: Optional[str]
    connection_requests:List[str] = []
    connections: List[str] = []

    # use settings
    class Settings:
        collection = "users"

class RequestConnectionModel(Document):
    user_id: str = ""
    connection_id: str = ""
    status: str = ""
    time: str = ""
    date: str = ""

    # use settings
    class Settings:
        collection = "request_connections"

