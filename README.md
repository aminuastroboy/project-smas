School ERP Backend

Quickstart:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuperuser
6. docker run -p 6379:6379 -d redis:7
7. celery -A school worker -l info
8. python manage.py runserver
