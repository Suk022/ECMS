from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """User registration schema."""
    name: str = Field(..., min_length=1, description="Full name")
    email: str = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    phone: Optional[str] = Field(None, description="Phone number")
    age: Optional[int] = Field(None, description="Patient age")
    gender: Optional[str] = Field(None, description="Patient gender")
    address: Optional[str] = Field(None, description="Patient address")


class UserResponse(BaseModel):
    """User response schema."""
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class LogoutRequest(BaseModel):
    """Logout request schema."""
    refresh_token: str
