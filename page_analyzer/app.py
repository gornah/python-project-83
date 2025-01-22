from .config import SECRET_KEY
from .url_utils import validate, normalize_url, get_check_data
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    request,
    redirect,
    url_for
)
from .db_manager import (
    get_url,
    get_url_list,
    add_url_to_base,
    add_check_to_base,
    get_urls_with_checks
)


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

# if not app.config['SECRET_KEY']:
#     raise RuntimeError("SECRET_KEY is not set. Check your env variables.")


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls():
    input_url = request.form.get('url')
    errors = validate(input_url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            input_url=input_url
            ), 422
    url = normalize_url(input_url)
    existing_url = get_url('name', url)
    if existing_url:
        flash('Страница уже существует', 'info')
        id = existing_url.id
        return redirect(url_for('url_details', id=id))
    add_url_to_base(url)
    id = get_url('name', url).id
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_details', id=id))


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
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_details', id=id))
    add_check_to_base(id, check_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_details', id=id))
