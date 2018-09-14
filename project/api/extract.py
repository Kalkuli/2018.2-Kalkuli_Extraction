import pytesseract
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from project import app
from pdf2image import convert_from_bytes
from PIL import Image


UPLOAD_FOLDER = os.path.relpath('./../assets')
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'File not found'
        file = request.files['file']
        if file.filename == '':
            return 'Empty file'
        if not allowed_file(file.filename):
            return 'Wrong extension'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            convert_pdf = convert_from_bytes(file.read())
            for page in convert_pdf:
                print(pytesseract.image_to_string(page, lang='por'))
            return file
