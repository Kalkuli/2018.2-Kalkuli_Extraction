import pytesseract
import os, time
import pickle
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, NotAcceptable
from project import app
from pdf2image import convert_from_bytes
from PIL import Image
from celery import shared_task


UPLOAD_FOLDER = os.path.relpath('./project/assets')
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@shared_task
def extraction_task(filename):
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
    convert = convert_pdf(file)
    json_text = extract_pdf(convert)
    return {
        "json_text": json_text,
        "filename": filename
    }

def view(error):
    if error == -1:
        raise NotFound()
    elif error == -2:
        raise BadRequest()
    elif error == -3:
        raise NotAcceptable()


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
def central():
    if request.method == 'POST':
        if 'file' not in request.files:
            error = -1
            try:
                return view(error)
            except HTTPException as e:
                return e
        file = request.files['file']
        if file.filename == '':
            error = -2
            try:
                return view(error)
            except HTTPException as e:
                return e
        if not allowed_file(file.filename):
            error = -3
            try:
                return view(error)
            except HTTPException as e:
                return e
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            task = extraction_task.delay(filename)
            # json_text = extract_pdf(convert)
            return jsonify({'location': url_for('get_status',
                                            task_id=task.id)}), 202
            # return jsonify({'raw_text': json_text}), 200

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
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], task.info['filename']))
    else:
        response = {
            'state': task.state
        }
    return jsonify(response), 200