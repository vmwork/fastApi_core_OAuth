import uuid 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db.repository.category import CategoryRepository
from schemas.category import CategoryCreate, CategoryUpdate, ShowCategory
from apis.v1.route_login import get_current_user
from models.user import User
from db.repository.blog import get_blogs_by_category
from schemas.blog import ShowBlog


router = APIRouter(prefix="/blogs/categories", tags=["Category"])



@router.get("", response_model=List[ShowCategory])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить все категории"""
    repo = CategoryRepository(db)
    return repo.get_all(skip, limit)


@router.get("/{category_id}", response_model=ShowCategory)
def get_category(
    category_id: uuid.UUID,  
    db: Session = Depends(get_db)
):
    """Получить категорию по ID"""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("", response_model=ShowCategory, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создать новую категорию (только для авторизованных)"""
    repo = CategoryRepository(db)
    
   
    existing = repo.get_by_slug(category.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists"
        )
    
    return repo.create(category)


@router.put("/{category_id}", response_model=ShowCategory)
def update_category(
    category_id: uuid.UUID, 
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновить категорию (только для авторизованных)"""
    repo = CategoryRepository(db)
    category = repo.update(category_id, category_update)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить категорию (только для авторизованных)"""
    repo = CategoryRepository(db)
    if not repo.delete(category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None


@router.get("/{category_id}/blogs", response_model=List[ShowBlog])
def get_blogs_in_category(
    category_id: uuid.UUID, 
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить все блоги в категории"""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Получаем блоги по категории
    blogs = get_blogs_by_category(category_id, db, skip, limit)
    return blogs
