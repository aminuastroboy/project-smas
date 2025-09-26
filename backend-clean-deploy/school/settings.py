import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
    'django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','corsheaders','users','exams','reports',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'school.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR / 'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}
}]
WSGI_APPLICATION = 'school.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_USER_MODEL = 'users.User'
STATIC_URL = '/static/'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework_simplejwt.authentication.JWTAuthentication',)}
SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),'REFRESH_TOKEN_LIFETIME': timedelta(days=1)}
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND','django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST','')
EMAIL_PORT = int(os.getenv('EMAIL_PORT','587') or 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD','')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL','school@example.com')
CELERY_BROKER_URL = os.getenv('REDIS_URL','redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL','redis://localhost:6379/0')
CORS_ALLOW_ALL_ORIGINS = True
