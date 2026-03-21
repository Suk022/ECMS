from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, UserRole
from models import UserRole as UserRoleEnum
from .auth import verify_token

# HTTP Bearer scheme for token extraction
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Authenticate user and return current user from database.
    
    Args:
        credentials: Bearer token from Authorization header
        db: Database session
        
    Returns:
        User object from database
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    # Verify and decode token
    token = credentials.credentials
    payload = verify_token(token)
    
    # Extract user ID from token
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def require_doctor(current_user: User = Depends(get_current_user)) -> User:
    """
    Require current user to have DOCTOR role.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User object if role is DOCTOR
        
    Raises:
        HTTPException: 403 if user is not a doctor
    """
    if current_user.role != UserRoleEnum.DOCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Doctor role required"
        )
    return current_user


async def require_receptionist(current_user: User = Depends(get_current_user)) -> User:
    """
    Require current user to have RECEPTIONIST role.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User object if role is RECEPTIONIST
        
    Raises:
        HTTPException: 403 if user is not a receptionist
    """
    if current_user.role != UserRoleEnum.RECEPTIONIST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Receptionist role required"
        )
    return current_user


async def require_patient(current_user: User = Depends(get_current_user)) -> User:
    """
    Require current user to have PATIENT role.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User object if role is PATIENT
        
    Raises:
        HTTPException: 403 if user is not a patient
    """
    if current_user.role != UserRoleEnum.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Patient role required"
        )
    return current_user
