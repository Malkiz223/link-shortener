import re

from flask import Flask, render_template, request, redirect, jsonify

import url_converter
from settings import DOMAIN_NAME, HYPERTEXT_PROTOCOL

app = Flask(__name__)


@app.get('/')
def index_get():
    return render_template('login.html')


@app.post('/')
def index_post():
    """
    Функция сокращает ссылку пользователя. Работает через AJAX, при нажатии на кнопку "Сократить"
    посылается POST-запрос в корень сайта со ссылкой long_url от юзера.
    Проводятся различные проверки на правильность URL, если всё хорошо -
    ссылка отправляется в базу и возвращает короткую ссылку из базы.
    """
    # то, что прилетает от AJAX
    long_url = request.form.get('long_url')
    if not long_url:
        return jsonify({'error': 'Ссылка не может быть пустой'})
    long_url = long_url.strip()

    has_dot_regexp = r'\w+[.]\w\w+'  # имеет символ до точки и минимум два символа после точки
    has_any_spaces_regexp = r'\s+'  # имеет пробельные символы в ссылке
    has_a_dot_and_two_characters_after = re.search(has_dot_regexp, long_url)
    has_any_spaces = re.search(has_any_spaces_regexp, long_url)
    if not has_a_dot_and_two_characters_after or has_any_spaces:
        return jsonify({'error': 'Некорректная ссылка'})

    # имеет в ссылке собственное доменное имя
    has_own_url = re.match(rf'{DOMAIN_NAME}', long_url.lower()) or re.match(
        rf'{HYPERTEXT_PROTOCOL + DOMAIN_NAME}', long_url.lower())
    if has_own_url:
        return jsonify({'error': 'Нельзя сокращать ссылку на сам сайт'})

    # если все проверки выше пройдены - ссылка отправляется в базу, возвращая сокращённую ссылку
    short_url = url_converter.convert_to_short_url(long_url)
    return jsonify({'message': HYPERTEXT_PROTOCOL + short_url})


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    """
    Функция идёт в базу и ищет там комбинацию символов, равной ссылке, которая пришла от пользователя.
    Если комбинация находится - возвращает ссылку, которая привязана к ней. В противном случае возвращает 404.
    """
    long_url = url_converter.convert_to_long_url(short_url)
    if long_url:
        return redirect(long_url)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
