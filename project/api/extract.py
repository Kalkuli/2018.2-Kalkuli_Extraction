import pytesseract
import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from project import app
from pdf2image import convert_from_bytes
from PIL import Image


UPLOAD_FOLDER = os.path.relpath('./../assets')
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_pdf(convert):
    text_obj = {}
    text_obj['text'] = []
    for page in convert:
        text_obj['text'].append(pytesseract.image_to_string(page, lang='por'))
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
            return jsonify({
                'message': 'File not found',
                'code': 400
            })
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'message': 'File not sent', 
                'code': 400
            })
        if not allowed_file(file.filename):
            return jsonify({
                'message': 'Not allowed file extension',
                'code': 400
            })
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            convert = convert_pdf(file)
            json_text = extract_pdf(convert)
            return jsonify({
                'raw_text': json_text
            })

#passar returns pra json
#desacoplar código 
