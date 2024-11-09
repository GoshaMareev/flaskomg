FROM python:3.9-slim

# Установка зависимостей для psycopg2 и psql (PostgreSQL client)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копирование всего проекта в контейнер
COPY . .

# Копирование файла .env
COPY .env ./

# Указываем команду для запуска приложения
CMD ["python", "app.py"]

