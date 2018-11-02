import pytesseract
import os
import time
import pickle
from flask import Flask, request, url_for, jsonify
from werkzeug.utils import secure_filename
from project import app
from pdf2image import convert_from_bytes
from PIL import Image
from celery import shared_task


UPLOAD_FOLDER = os.path.relpath('./project/assets')
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@shared_task
def extraction_task(filename):
    while not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        time.sleep(0.1)
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
    convert = convert_pdf(file)
    json_text = extract_pdf(convert)
    return {
        "json_text": json_text,
        "filename": filename
    }


def extract_pdf(convert):
    text_obj = {}
    text_obj['raw_text'] = ""
    for page in convert:
        text_obj['raw_text'] += pytesseract.image_to_string(page, lang='por')
    return text_obj


def convert_pdf(file):
    return convert_from_bytes(file.read())


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({
            "Status": "Fail",
            "Error": "No file sent"
        }), 422
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({
            "Status": "Fail",
            "Error": "Extension not allowed. Use PDF."
        }), 415

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    task = extraction_task.delay(filename)
    return jsonify({'location': url_for('get_status',
                                        task_id=task.id)}), 202


@app.route('/status_extraction/<task_id>')
def get_status(task_id):
    task = extraction_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state
        }
        if 'raw_text' in task.info['json_text']:
            response['raw_text'] = task.info['json_text']['raw_text']
            os.remove(os.path.join(
                app.config['UPLOAD_FOLDER'], task.info['filename']))
    else:
        response = {
            'state': task.state
        }
    return jsonify(response), 200
