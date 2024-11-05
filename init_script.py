import os
import psycopg2
from psycopg2 import sql

# Получение параметров подключения из переменных окружения
DB_URL = os.getenv('DATABASE_URL', 'postgresql://flasktest:Password1!@localhost:5432/fl_test')


def init_db():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Создание таблицы users, если она не существует
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized.")
