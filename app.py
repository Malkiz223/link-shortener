from flask import Flask, render_template, request

"""
Необходимо создать базу, в которую будем помещать ссылки от пользователей (проверять на наличие точки через regexp?)
При переходе по /<short_link> делать селект из БД и возвращать значение full_link в качестве перенаправления
Сделать базу сгенерированных линков
"""

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        long_link = request.form.get('long_link')  # запрос к данным формы
        message = f'Вижу твою ссылку, это {long_link}'

    return render_template('login.html', message=message)


@app.route('/<short_link>/')
def short_link(link=None):
    print(link)


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(debug=True)
