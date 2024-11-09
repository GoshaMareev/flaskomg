from flask import Flask, render_template, redirect, url_for, flash
from forms import NameForm
import psycopg2
from psycopg2 import sql
from config import Config
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# URL-кодирование пароля для корректного подключения
password = quote_plus(os.getenv('DB_PASSWORD', 'Password1!'))
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER', 'flasktest')}:{password}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'fl_test')}"

# подключение к базе данных
def get_db_connection():
    try:
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        print("Успешное подключение к базе данных")
        cur = conn.cursor()
        # Создание таблицы, если она не существует
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e.pgcode}, {e.pgerror}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        conn = get_db_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                # Проверка существования таблицы
                cur.execute("SELECT to_regclass('public.users');")
                table_exists = cur.fetchone()[0]
                print(f"Таблица существует: {table_exists}")

                if table_exists is None:
                    flash('Ошибка: Таблица "users" не существует.')
                else:
                    # Добавление имени в таблицу
                    cur.execute(sql.SQL("INSERT INTO public.users (name) VALUES (%s)"), [name])
                    conn.commit()
                    flash('Имя успешно добавлено!')
                    print("Имя успешно добавлено!")

            except Exception as e:
                flash(f'Ошибка добавления имени: {e}')
            finally:
                cur.close()
                conn.close()
        else:
            flash('Не удалось подключиться к базе данных.')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
