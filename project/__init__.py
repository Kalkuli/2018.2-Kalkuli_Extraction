from flask import Flask, jsonify

app = Flask(__name__)

app.config.from_object('project.config.DevelopmentConfig')

import project.api.extract


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({
        'data': 'Welcome to Extraction Service!'
    })