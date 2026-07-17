#!/bin/sh

set -e

echo "===================================================="
echo "🚀 Запуск чистого развертывания FastBlog API..."
echo "===================================================="

echo "🧹 Очистка фантомного кэша .pyc и __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete


echo "⏳ Ожидание полной готовности базы данных PostgreSQL..."
until pg_isready -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
    printf '.'
    sleep 1
done
echo -e "\n🟢 База данных готова к работе!"

echo "⚙️ Применение миграций базы данных (UUID v7 schema)..."
cd /app/backend && alembic upgrade head

echo "🌱 Запуск наполнения базы данных начальными данными..."
python seed.py

echo "===================================================="
echo "🎉 Развертывание успешно завершено!"
echo "📱 Приложение доступно по адресу: http://localhost:8000"
echo "📑 Документация API (Swagger UI): http://localhost:8000/docs"
echo "===================================================="
echo "📜 Логи сервера:"

exec "$@"
