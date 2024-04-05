import os
import shutil
from datetime import datetime
from subprocess import Popen, PIPE
from io import StringIO
from flask import Flask, jsonify, request, make_response
import sys
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/files'


@app.route('/api/interpreter/<user_name>', methods=['GET', 'POST'])
def interpreter(user_name):
    def exec_sented_file(file, name, sent_time):
        file.save(r'interpreted_files\{}.txt'.format(rf'{sent_time}_{name}'))
        out, err = Popen(r'python interpreted_files\{}.txt'.format(
            rf'{sent_time}_{name}'), shell=True, stdout=PIPE, stdin=PIPE,
            stderr=PIPE).communicate()

        # print(out.decode(), end='')
        # print(err.decode(), end='')

        if out:
            return out.decode()
        return f'{out.decode()}{err.decode()}'

    if request.method == 'POST':
        sent_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if request.files:
            print(request.data)
            if not request.files.get('key'):
                return 'Key File Error'
            if not user_name:
                return 'Name Not Found Error'

            file = request.files['key']
            print(type(user_name))
            return_file = exec_sented_file(file, user_name, sent_time)
            return f'{return_file}'
    return "Method Error"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(415)
def bad_media(_):
    return make_response(jsonify({'error': 'Unsupported Media Type'}), 415)


def main():
    app.run(port=8080, host='127.0.0.1')


def troll():
    return 'troll'


if __name__ == '__main__':
    main()
