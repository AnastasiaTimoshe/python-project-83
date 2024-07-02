from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort,
)
from page_analyzer.database import DatabaseManager
from page_analyzer.validate import validate, normalize_url
from page_analyzer.html import extract_page_data
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

db_manager = DatabaseManager(app)


@app.get('/')
def index():
    return render_template('index.html',)


@app.post('/urls')
def show_url_page():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    url_id = db_manager.find_url_by_name(normal_url)
    error = validate(url)

    if error:
        flash(error, 'danger')
        return render_template('index.html'), 422

    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url_list', id=url_id))
    new_url = db_manager.insert_url(normal_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_list', id=new_url.id))


@app.get('/urls')
def urls():
    urls_data = db_manager.get_all_urls()
    return render_template('urls/list.html', urls=urls_data)


@app.get('/urls/<int:id>')
def get_url_list(id):
    url_item = db_manager.find_url_by_id(id)
    checks = db_manager.find_checks_by_id(id)
    if url_item:
        return render_template('urls/detail.html', url_item=url_item,
                               checks=checks,)
    return render_template('errors/404.html',), 404


@app.post('/urls/<int:id>/checks')
def show_url_checks(id):
    url_item = db_manager.find_url_by_id(id)
    if not url_item:
        abort(404)

    try:
        response = requests.get(url_item.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url_list', id=id))

    result_check = extract_page_data(response.text)
    result_check['url_id'] = id
    result_check['status_code'] = response.status_code
    db_manager.add_check(id, result_check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_list', id=id))


@app.errorhandler(404)
def page_404(e):
    return render_template('errors/404.html',), 404


@app.errorhandler(500)
def page_500(e):
    return render_template('errors/500.html',), 500
