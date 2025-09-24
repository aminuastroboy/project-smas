web: gunicorn school_backend.wsgi --log-file -
worker: celery -A school_backend worker -l info
