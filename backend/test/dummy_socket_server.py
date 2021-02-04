from flask import Flask
from flask_socketio import SocketIO, send


def start_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.debug = True
    # socketio = SocketIO(app, cors_allowed_origins=['localhost'])
    socketio = SocketIO(app, cors_allowed_origins='*')

    @socketio.on('start')
    def on_connect(data):
        print('start', data)
        send('answer to connection')

    socketio.run(app, host='0.0.0.0', port='5555')


if __name__ == '__main__':
    start_app()
