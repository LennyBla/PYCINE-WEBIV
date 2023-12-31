from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    movies = relationship("Movie", back_populates="user")  # Adicione esta linha


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer)
    title = Column(String)  
    image = Column(String)  
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="movies")
    
    