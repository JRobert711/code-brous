from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Esquemas base
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Esquema para crear usuario
class UserCreate(UserBase):
    password: str

# Esquema para respuesta (sin password)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para token
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None