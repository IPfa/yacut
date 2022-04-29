import random
import string

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map

ACCEPTABLE_VALUES = string.ascii_lowercase + string.digits
BASE_URL = 'http://localhost/'


def get_unique_short_id():
    rand_short_id = random.choices(ACCEPTABLE_VALUES, k=6)
    return ''.join(rand_short_id)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_oroginal_id(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or not data['custom_id']:
        short_url = get_unique_short_id()
    else:
        short_url = data['custom_id']
        for i in short_url:
            if i not in ACCEPTABLE_VALUES:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URL_map.query.filter_by(short=short_url).first() is not None:
            raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')
    url_map = URL_map(
        original=data['url'],
        short=short_url
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': BASE_URL + url_map.short
    }), 201
