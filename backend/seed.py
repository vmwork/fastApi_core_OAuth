import uuid
from db.session import SessionLocal
from models.user import User
from models.blog import Blog          
from models.category import Category 
from core.hashing import Hasher

def seed_superuser():
    db = SessionLocal()
    try:
        # Ищем пользователя по email
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        if not admin:
            print("🚀 СИД: Создание дефолтного суперадмина...")
            new_admin = User(
                id=uuid.uuid4(),
                email="admin@example.com",
                password=Hasher.get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(new_admin)
            db.commit()
            print("🟢 СИД: Суперадмин успешно создан! (admin@example.com / admin123)")
        
        # 🟢 ЕСЛИ ЮЗЕР ЕСТЬ, НО ОН НЕ АДМИН — ПРИНУДИТЕЛЬНО ВЫДАЕМ ПРАВА
        elif not admin.is_superuser:
            print("🔄 СИД: Пользователь существует, но не имеет прав админа. Обновление...")
            admin.is_superuser = True
            admin.is_active = True
            # На всякий случай сбрасываем пароль на дефолтный, чтобы не запутаться
            admin.password = Hasher.get_password_hash("admin123")
            db.commit()
            print("🟢 СИД: Права суперадмина успешно выданы существующему пользователю!")
            
        else:
            print("ℹ️ СИД: Суперадмин уже существует в базе и имеет полные права.")
            
    except Exception as e:
        print(f"❌ СИД: Ошибка при обработке админа: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_superuser()
