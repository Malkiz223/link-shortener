from flask import Flask, render_template, request, redirect, jsonify
import long_to_short_url
import short_to_long_url

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')  # запрос к данным формы
        if not long_url:
            return jsonify({'error': 'Введите, пожалуйста, URL'})
        short_url_for_user = long_to_short_url.make_a_short_url(long_url)
        return jsonify({'message': short_url_for_user})
    return render_template('login.html')


@app.route('/<short_url_from_user>')
def short_url(short_url_from_user):
    long_url = short_to_long_url.return_original_url_from_short(short_url_from_user)
    if long_url:
        return redirect(long_url)
    return 'Такой ссылки нет :(', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
