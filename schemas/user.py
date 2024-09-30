from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    address: str
    email: str

    
class userResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str