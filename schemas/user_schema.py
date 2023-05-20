from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    username: str
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[str]
    educational_details: Optional[str]
    # email_address: Optional[str]
    contact_no: Optional[int]
    skills: List[str] = []
    internship_details: List[str] = []
    yoj: Optional[int]
    yop: Optional[int]
    department: Optional[str]
    course: Optional[str]
    current_semeseter: Optional[int]
    bio: Optional[str]
    address: Optional[str]
    hostel: Optional[str]
    connection_requests: Optional[List[str]]
    connections: Optional[List[str]]

class RegisterSchema(BaseModel):
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class ConnectionRequestSchema(BaseModel):
    username: str
    connection_username: str

class SearchSchema(BaseModel):
    search_query: str

