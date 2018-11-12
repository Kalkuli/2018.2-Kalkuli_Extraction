import os
from flask import Flask, jsonify
from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL')
    )
    celery.conf.update(broker_pool_limit=0)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Instantiate the app and Celery
app = Flask(__name__)
celery = make_celery(app)

# Set Configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# Register blueprint(s)
from project.api.views import extraction_blueprint
app.register_blueprint(extraction_blueprint)