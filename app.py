from flask import Flask, render_template, request, redirect
import long_to_short_url
import short_to_long_url

"""
Необходимо создать базу, в которую будем помещать ссылки от пользователей (проверять на наличие точки через regexp?)
При переходе по /<short_link> делать селект из БД и возвращать значение full_link в качестве перенаправления
Сделать базу сгенерированных линков
"""

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def login():
    message = ''
    short_url = ''
    if request.method == 'POST':
        long_url = request.form.get('long_url')  # запрос к данным формы
        if not long_url:
            return 'Пожалуйста, введите URL'
        short_url = long_to_short_url.make_a_short_url(long_url)
        return short_url
    return render_template('login.html', message=message, short_url=short_url)


@app.route('/<short_url>/')
def short_url(short_url):
    long_url = short_to_long_url.return_original_url_from_short(short_url)
    if long_url:
        return redirect(f'{long_url}')
    return 'Такой ссылки нет :('


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True)
