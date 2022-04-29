import random
import string

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_Map_Form
from .models import URL_map


def get_unique_short_id():
    choices = string.ascii_letters + string.digits
    rand_short_id = random.choices(choices, k=6)
    return ''.join(rand_short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_Map_Form()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short_link = get_unique_short_id()
        else:
            short_link = form.custom_id.data
            if URL_map.query.filter_by(short=short_link).first() is not None:
                flash(f'Имя {short_link} уже занято!', 'not-unique-short')
                return render_template('url_cutter.html', form=form)
        url_map = URL_map(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(url_map)
        db.session.commit()
        message = 'Ваша новая ссылка готова:'
        return render_template('url_cutter.html', short_link=short_link, message=message, form=form)
    return render_template('url_cutter.html', form=form)


@app.route('/<string:short_id>')
def resource_redirect(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if not url_map:
        abort(404)
    real_link = str(url_map.original)
    return redirect(real_link)
