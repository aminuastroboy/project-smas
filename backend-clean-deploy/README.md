Clean backend package (Django) with exams + reports + Celery integration.

Quick start:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuperuser
6. run redis (eg: docker run -p 6379:6379 -d redis:7)
7. celery -A school worker -l info
8. python manage.py runserver

API endpoints:
- POST /api/exams/<exam_id>/submit/
- GET /api/exams/my-results/
- POST /api/reports/send/<class_id>/
- GET /api/reports/status/<task_id>/


## Deployment manifests added
- Dockerfile: containerize the Django app for Railway
- Procfile: process for Railway environment
- railway.json: Railway config-as-code manifest
- .github/workflows/deploy-backend-railway.yml: GitHub Actions workflow to deploy backend to Railway (requires RAILWAY_TOKEN secret)
- .github/workflows/deploy-frontend-vercel.yml: GitHub Actions workflow to deploy frontend to Vercel (requires VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID secrets)
