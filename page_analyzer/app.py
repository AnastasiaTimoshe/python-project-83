import os
from flask import (
    Flask,
    abort,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    get_flashed_messages
)
from page_analyzer.validate import validate_url, normalize_url
from page_analyzer.html import make_check
from page_analyzer.database import (
    create_connection,
    get_url_by_id,
    get_url_by_name,
    show_url,
    show_urls,
    show_url_checks,
    add_url,
    add_url_check
)
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def first_page():
    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


@app.get('/urls')
def get_urls():
    conn = create_connection(DATABASE_URL)
    try:
        messages = get_flashed_messages()
        urls = show_urls(conn)
        url_checks = show_url_checks(conn)

        url_data = []
        for url in urls:
            url_id = url['id']
            check = next((check for check in url_checks if check['url_id'] == url_id), {})
            url_data.append({
                'id': url_id,
                'name': url['name'],
                'last_check': check.get('created_at'),
                'status_code': check.get('status_code')
            })

        return render_template('show_urls.html', messages=messages, urls=url_data)
    finally:
        conn.close()


@app.post('/urls')
def post_url():
    conn = create_connection(DATABASE_URL)
    try:
        url_new = request.form.get('url')
        error_message = validate_url(url_new)
        if error_message:
            flash(error_message)
            return render_template('index.html'), 422
        url_norm = normalize_url(url_new)
        url = get_url_by_name(conn, url_norm)
        if url:
            flash('Страница уже существует')
            id = url.id
        else:
            flash('Страница успешно добавлена')
            id = add_url(conn, url_norm)
        return redirect(url_for('get_url', id=id))
    finally:
        conn.close()


@app.get('/urls/<int:id>')
def get_url(id):
    conn = create_connection(DATABASE_URL)
    try:
        url = get_url_by_id(conn, id)
        if not url:
            return render_template('404.html'), 404
        messages = get_flashed_messages(with_categories=True)
        checks = show_url(conn, id)
        return render_template('show_url.html', url=url, messages=messages, checks=checks)
    finally:
        conn.close()


@app.post('/urls/<int:url_id>/checks')
def get_check(url_id):
    conn = create_connection(DATABASE_URL)
    try:
        url = get_url_by_id(conn, url_id)
        check_dict = make_check(url.name, url.id)
        if check_dict['status_code'][0] != 200:
            flash('Произошла ошибка при проверке')
        else:
            flash('Страница успешно проверена')
        add_url_check(conn, check_dict)
        return redirect(url_for('get_url', id=url.id))
    finally:
        conn.close()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
