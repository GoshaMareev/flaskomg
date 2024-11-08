from flask import Flask, render_template, redirect, url_for, flash
from forms import NameForm
import psycopg2
from psycopg2 import sql
from config import Config
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # default_secret_key

# Соединение с базой данных
def get_db_connection():
    try:
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        print("Успешное подключение к базе данных")
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
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
                print("Проверка существования таблицы...")
                cur.execute("SELECT to_regclass('public.users');")
                table_exists = cur.fetchone()[0]
                print(f"Таблица существует: {table_exists}")

                if table_exists is None:
                    flash('Ошибка: Таблица "users" не существует.')
                else:
                    print("Вставка имени в таблицу...")
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

