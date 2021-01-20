#!/bin/env python
from app import create_app, socketio
import json

if __name__ == '__main__':
    with open('./config.json', 'r') as config_file:
        config = json.loads(config_file.read())
        app = create_app(configs=[config['COMMON'], config['TEST']])
        socketio.run(app, host='0.0.0.0', port=5551)