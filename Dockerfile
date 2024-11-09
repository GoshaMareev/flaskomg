FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

р
COPY . .

# Копирование .env файла
COPY .env ./

# Запуск приложения
CMD ["python", "app.py"]

