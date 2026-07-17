from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
)
    create_tables()
    include_router(app)
    return app


app = start_application()


@app.get("/", tags=["System"])
def home():
    return {"msg": "Hello FastAPI Auth🚀"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Auth🚀",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
