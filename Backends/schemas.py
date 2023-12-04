from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

class MovieBase(BaseModel):
    tmdb_id: int
    user_id: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
