import uuid
from typing import List
from models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError 
from db.session import get_db
from schemas.user import UserCreate, ShowUser
from db.repository.user import create_new_user, list_all_users, toggle_user_status
from apis.v1.route_login import get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_new_user(user=user, db=db)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

@router.get("", response_model=List[ShowUser])
def get_users_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Получить список всех пользователей (Только для Админа)"""
    return list_all_users(db=db, skip=skip, limit=limit)

@router.patch("/{user_id}/toggle-active", response_model=ShowUser)
def change_user_activity(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Включить/выключить активность пользователя (Только для Админа)"""
    user = toggle_user_status(user_id=user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user
