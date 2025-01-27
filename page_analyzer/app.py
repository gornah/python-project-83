import requests
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from .config import SECRET_KEY
from .db_manager import (
    add_check,
    add_url,
    get_url,
    get_url_list,
    get_urls_with_checks,
)
from .parser import get_check_data
from .url_utils import normalize_url, validate

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls():
    input_url = request.form.get('url')
    errors = validate(input_url)
    if errors:
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            input_url=input_url
            ), 422

    url = normalize_url(input_url)
    existing_url = get_url('name', url)

    if existing_url:
        flash('Страница уже существует', 'info')
        id = existing_url.id
        return redirect(url_for('url_details', id=id))

    id = add_url(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_details', id=id)), 302


@app.get('/urls')
def get_urls():
    url_list = get_url_list()
    return render_template('urls.html', url_list=url_list)


@app.get('/urls/<int:id>')
def url_details(id: int):
    messages = get_flashed_messages(with_categories=True)
    data = get_urls_with_checks(id)
    return render_template('url_details.html', data=data, messages=messages)


@app.post('/urls/<int:id>/checks')
def url_checks(id: int):
    url = get_url('id', id).name
    try:
        check_data = get_check_data(url)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_details', id=id))
    add_check(id, check_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_details', id=id)), 302
