import os
from flask import (
    Flask,
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
    show_urls,
    show_url,
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
    return render_template("index.html", messages=messages)


@app.get('/urls')
def get_urls():
    with create_connection(DATABASE_URL) as conn:
        messages = get_flashed_messages()
        urls = show_urls(conn)
        url_checks = show_url_checks(conn)

        url_data = [
            {
                'id': url['id'],
                'name': url['name'],
                'last_check': next(
                    (check.get('created_at') for check in url_checks if check['url_id'] == url['id']), None
                ),
                'status_code': next(
                    (check.get('status_code') for check in url_checks if check['url_id'] == url['id']), None
                )
            }
            for url in urls
        ]

        return render_template('show_urls.html', messages=messages, urls=url_data)


@app.post('/urls')
def post_url():
    url_new = request.form.get('url')
    error_message = validate_url(url_new)
    if error_message:
        flash(error_message)
        return render_template('index.html'), 422

    url_norm = normalize_url(url_new)
    with create_connection(DATABASE_URL) as conn:
        url = get_url_by_name(conn, url_norm)
        if url:
            flash('Страница уже существует')
            id = url['id']
        else:
            flash('Страница успешно добавлена')
            id = add_url(conn, url_norm)
            conn.commit()
        return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    with create_connection(DATABASE_URL) as conn:
        url = get_url_by_id(conn, id)
        if not url:
            return render_template('error/404.html'), 404

        messages = get_flashed_messages(with_categories=True)
        checks = show_url(conn, id)
        return render_template('show_url.html', url=url, messages=messages, checks=checks)


@app.post('/urls/<int:id>/checks')
def post_url_check(id: int):
    conn = create_connection(DATABASE_URL)
    try:
        url = get_url_by_id(conn, id)
        if not url:
            return render_template('error/404.html'), 404

        page_data = make_check(url['name'], id)
        if page_data is None:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('get_url', id=id))

        status_code = page_data.get('status_code')

        if status_code is not None and status_code < 400:
            page_data['url_id'] = id
            add_url_check(conn, page_data)
            conn.commit()
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'danger')

        return redirect(url_for('get_url', id=id))
    finally:
        conn.close()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    app.run()
