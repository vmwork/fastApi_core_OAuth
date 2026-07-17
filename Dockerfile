FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements из корня контекста сборки
COPY backend/requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Копируем всё содержимое (включая папку backend) в /app
COPY . /app

RUN chmod +x /app/backend/deploy.sh

EXPOSE 8000

ENTRYPOINT ["/app/backend/deploy.sh"]

# Запуск модуля backend.main из рабочей директории /app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
