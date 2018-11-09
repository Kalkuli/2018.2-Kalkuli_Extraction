import os
import time
import pickle

from PIL import Image

from flask import Flask, request, url_for, jsonify, Blueprint
from flask_cors import CORS
from werkzeug.utils import secure_filename
from celery import shared_task

from project.api.extraction import Extraction
from project.api.s3_utils import S3Utils
from project.api.helpers import allowed_file



extraction_blueprint = Blueprint('extraction', __name__)
CORS(extraction_blueprint)


@shared_task
def extraction_task(filename):
    s3 = S3Utils()
    response = s3.get_file(filename)
    file = response['Body'].read()
    extraction = Extraction(file)
    json_text = extraction.extract()
    return {
        "json_text": json_text,
        "filename": filename
    }


@extraction_blueprint.route('/extract', methods=['POST'])
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
    s3 = S3Utils()
    s3.upload_to_s3(file)
    task = extraction_task.delay(filename)
    return jsonify({'location': url_for('extraction.get_status',
                                        task_id=task.id)}), 202


@extraction_blueprint.route('/status_extraction/<task_id>')
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
    else:
        response = {
            'state': task.state
        }
    return jsonify(response), 200
