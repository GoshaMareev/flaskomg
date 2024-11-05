FROM ubuntu:latest
LABEL authors="maree"
# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Открываем порт
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]

ENTRYPOINT ["top", "-b"]