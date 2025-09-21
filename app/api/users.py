from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import User, UserUpdate
from app.crud import user as crud_user
from app.api.auth import get_current_active_user
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, 
               current_user: User = Depends(get_current_active_user),
               db: Session = Depends(get_db)):
    """Get list of users (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    users = db.query(crud_user.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, 
              current_user: User = Depends(get_current_active_user),
              db: Session = Depends(get_db)):
    """Get user by ID"""
    # Users can only view their own profile, unless they're admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate,
                current_user: User = Depends(get_current_active_user),
                db: Session = Depends(get_db)):
    """Update user"""
    # Users can only update their own profile, unless they're admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user