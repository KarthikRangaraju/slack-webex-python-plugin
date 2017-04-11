import os
from flask import Flask
from flask_classy import FlaskView
from webex_slash_command_controller import WebexSlashCommandController

app = Flask(__name__)
WebexSlashCommandController.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

