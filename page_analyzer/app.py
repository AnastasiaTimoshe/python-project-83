import os
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    abort
)
from page_analyzer.validate import validate_url, normalize_url
from page_analyzer.html import make_check
import page_analyzer.database as db
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def first_page():
    return render_template("index.html")


@app.get('/urls')
def get_urls():
    with db.create_connection(DATABASE_URL) as conn:
        urls_data = db.get_urls_data(conn)
        return render_template('show_urls.html', urls=urls_data)


@app.post('/urls')
def post_url():
    url_new = request.form.get('url')
    error_message = validate_url(url_new)
    if error_message:
        flash(error_message)
        return render_template('index.html'), 422

    url_norm = normalize_url(url_new)
    with db.create_connection(DATABASE_URL) as conn:
        url = db.get_url_by_name(conn, url_norm)
        if url:
            flash('Страница уже существует')
            id = url.id
        else:
            flash('Страница успешно добавлена')
            id = db.add_url(conn, url_norm)
            conn.commit()
        return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    with db.create_connection(DATABASE_URL) as conn:
        url = db.get_url_by_id(conn, id)
        if not url:
            abort(404)

        checks = db.get_url_checks(conn, id)
        return render_template('show_url.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def post_url_check(id: int):
    with db.create_connection(DATABASE_URL) as conn:
        url = db.get_url_by_id(conn, id)
        if not url:
            abort(404)

        page_data = make_check(url.name, id)
        if page_data is None:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('get_url', id=id))

        status_code = page_data.get('status_code')

        if status_code is not None and status_code < 400:
            page_data['url_id'] = id
            db.add_url_check(conn, page_data)
            conn.commit()
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'danger')

        return redirect(url_for('get_url', id=id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    app.run()
