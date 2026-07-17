import uuid
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload 
from models.blog import Blog
from models.category import Category
from schemas.blog import CreateBlog, UpdateBlog
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: uuid.UUID):
    # Получаем категории, если указаны
    categories = []
    if blog.categories_id:
        categories = db.query(Category).filter(Category.id.in_(blog.categories_id)).all()
    
    # Создаем блог
    blog_data = blog.model_dump(exclude={'categories_id'})
    db_blog = Blog(**blog_data, author_id=author_id)
    db_blog.categories = categories
    
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def retreive_blog(id: uuid.UUID, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def get_blog_by_slug(slug: str, db: Session):
    blog = db.query(Blog).filter(Blog.slug == slug).first()
    return blog




def list_blogs(db: Session, skip: int = 0, limit: int = 100, published_only: bool = False):
    query = db.query(Blog).options(joinedload(Blog.categories))
    if published_only:
        query = query.filter(Blog.published == True)
    return query.offset(skip).limit(limit).all()





def get_blogs_by_category(category_id: uuid.UUID, db: Session, skip: int = 0, limit: int = 100):
    blogs = db.query(Blog).join(Blog.categories).filter(Category.id == category_id).offset(skip).limit(limit).all()
    return blogs


def update_blog(id: uuid.UUID, blog: UpdateBlog, author_id: uuid.UUID, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog"}
    
    update_data = blog.model_dump(exclude_unset=True, exclude={'categories_id'})
    for field, value in update_data.items():
        setattr(blog_in_db, field, value)
    
    if blog.categories_id is not None:
        categories = db.query(Category).filter(Category.id.in_(blog.categories_id)).all()
        blog_in_db.categories = categories
    
    db.add(blog_in_db)
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db


def delete_blog(id: uuid.UUID, author_id: uuid.UUID, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete a blog"}
    blog_in_db.delete()
    db.commit()
    return {"msg": f"deleted blog with id {id}"}


def approve_blog_publication(id: uuid.UUID, db: Session) -> Optional[Blog]:
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if blog_in_db:
        blog_in_db.published = True
        blog_in_db.is_active = True
        db.commit()
        db.refresh(blog_in_db)
    return blog_in_db
