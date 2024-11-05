from flask import Flask, render_template, redirect, url_for, flash
from forms import NameForm
import psycopg2
from psycopg2 import sql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ

# Соединение с базой данных
def get_db_connection():
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        conn = get_db_connection()
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(sql.SQL("INSERT INTO public.users (name) VALUES (%s)"), [name])
                conn.commit()
                flash('Имя успешно добавлено!')
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
    app.run(debug=True)
