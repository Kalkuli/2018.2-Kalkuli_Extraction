from flask import Flask, jsonify

app = Flask(__name__)

app.config.from_object('project.config.DevConfig')

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({
        'data': 'Welcome to Flask!'
    })