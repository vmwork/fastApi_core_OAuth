import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Fast API Auth 🔥"
    PROJECT_VERSION: str = "1.0.0"

    PROJECT_DESCRIPTION: str = (
        "### 🔗 Разработчик: Vladyslav | Senior Fullstack Developer\n"
        "👉 [Profile on freelancehunt : vmarwork](https://freelancehunt.com/freelancer/vmarwork.html)"
    )

    # Задаем дефолтные значения прямо в getenv на случай, если .env не прочитался
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "postgres") # Внутри сети Docker имя сервиса - 'postgres'
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_auth")
    
    # Динамически собираем URL при каждом обращении
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
