import re

from flask import Flask, render_template, request, redirect, jsonify
import long_to_short_url
import settings
import short_to_long_url

app = Flask(__name__)


@app.get('/')
def index_get():
    return render_template('login.html')


@app.post('/')
def index_post():
    long_url = request.form.get('long_url').strip()
    if not long_url:
        return jsonify({'error': 'Ссылка не может быть пустой'})

    regexp = r'\w+[.]\w\w+'  # имеет символ до точки и минимум два символа после точки
    has_a_dot_and_two_characters_after = re.search(regexp, long_url)
    if not has_a_dot_and_two_characters_after:
        return jsonify({'error': 'Некорректная ссылка'})

    has_own_url = re.match(rf'{settings.DOMAIN_NAME}', long_url.lower()) or re.match(
        rf'{settings.HYPERTEXT_PROTOCOL + settings.DOMAIN_NAME}', long_url.lower())
    # имеет ссылку для сокращения на самого себя
    if has_own_url:
        return jsonify({'error': 'Нельзя сокращать ссылку на сам сайт'})

    short_url_for_user = long_to_short_url.make_a_short_url(long_url)
    return jsonify({'message': settings.HYPERTEXT_PROTOCOL + short_url_for_user})


@app.route('/<short_url_from_user>')
def short_url(short_url_from_user):
    long_url = short_to_long_url.return_original_url_from_short(short_url_from_user)
    if long_url:
        return redirect(long_url)
    return 'Такой ссылки нет :(', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
