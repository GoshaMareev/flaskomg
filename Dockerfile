FROM python:3.9-slim

# Установите зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установите зависимости Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Копируем файл .env
COPY .env ./

# Указываем команду для запуска приложения
CMD ["python", "app.py"]
