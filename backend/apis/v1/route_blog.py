import uuid 
from typing import List

from apis.v1.route_login import get_current_user, get_current_admin
from models.user import User
from db.repository.blog import create_new_blog
from db.repository.blog import delete_blog
from db.repository.blog import list_blogs
from db.repository.blog import retreive_blog
from db.repository.blog import update_blog
from db.repository.blog import approve_blog_publication
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from sqlalchemy.orm import Session

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/all", response_model=List[ShowBlog])
def get_every_single_blog(db: Session = Depends(get_db)):
    """Получить абсолютно все статьи (включая черновики)"""
    return list_blogs(db=db, published_only=False)


@router.get("", response_model=List[ShowBlog])
def get_published_blogs(db: Session = Depends(get_db)):
    """Получить только опубликованные статьи"""
    return list_blogs(db=db, published_only=True)

@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: uuid.UUID, db: Session = Depends(get_db)):
    blog = retreive_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog


@router.post("", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: CreateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blog = create_new_blog(blog=blog, db=db, author_id=current_user.id)
    return blog


@router.put("/{id}", response_model=ShowBlog)
def update_a_blog(
    id: uuid.UUID,
    blog: UpdateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blog = update_blog(id=id, blog=blog, author_id=current_user.id, db=db)
    if isinstance(blog, dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog

@router.patch("/{id}/approve", response_model=ShowBlog)
def approve_blog(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Опубликовать статью из черновика (Только для Админа)"""
    blog = approve_blog_publication(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog


@router.delete("/{id}")
def delete_a_blog(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = delete_blog(id=id, author_id=current_user.id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": f"Successfully deleted blog with id {id}"}
