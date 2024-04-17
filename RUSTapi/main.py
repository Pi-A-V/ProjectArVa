from datetime import datetime
from subprocess import Popen, PIPE
from flask import Flask, jsonify, request, make_response, send_from_directory
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/files'


@app.route('/api/interpreter/<user_name>', methods=['POST'])
def interpreter(user_name):
    def exec_sented_file(file, name, sent_time):
        file.save(r'interpreted_files\{0}\{1}.txt'.format(user_name,
                                                          rf'{sent_time}_{name}'))
        out, err = Popen(r'python interpreted_files\{0}\{1}.txt'.format(
            user_name, rf'{sent_time}_{name}'), shell=True, stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE).communicate()

        return f'{out.decode()}{err.decode()}'

    if request.method == 'POST':
        sent_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if request.files:
            if not request.files.get('key'):
                return 'Key File Error'
            if not user_name:
                return 'Name Not Found Error'
        if not os.path.isdir(r"interpreted_files/{}".format(user_name)):
            os.mkdir(r"interpreted_files/{}".format(user_name))

            file = request.files['key']
            return_file = exec_sented_file(file, user_name, sent_time)
            return f'{return_file}'
    return "Method Error"


@app.route('/api/interpreter_history/<user_name>', methods=['GET'])
def interpreter_history(user_name):
    if request.method == 'GET':
        if not os.path.isdir(r"interpreted_files/{}".format(user_name)):
            os.mkdir(r"interpreted_files/{}".format(user_name))
            return 'User Is Registered'

        files = ['_'.join(strs.split('_')[:2]) for strs in
                 os.listdir(r"interpreted_files/{}".format(user_name))]
        return {'main': files}
    return "Method Error"

@app.route('/api/interpreter_history/search/<date_time>/<user_name>', methods=['GET'])
def interpreter_history_search(date_time, user_name):
    if request.method == 'GET':
        if not os.path.isdir(r"interpreted_files/{}".format(user_name)):
            return 'User Isn`t Registered'

        if '{0}_{1}.txt'.format(date_time, user_name) in os.listdir(r"interpreted_files/{}".format(user_name)):
            return send_from_directory(r"interpreted_files/{}".format(user_name), '{0}_{1}.txt'.format(date_time, user_name))
        return "File Not Found"
    return "Method Error"



@app.errorhandler(404)
def not_found(_):
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
