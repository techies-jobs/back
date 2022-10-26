from .base import *

print("================== PRODUCTION MODE =======================")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1%2d7q2z(60ep0yu@+cx-r8@c4y8$!j130l-lc=xis9-#8qp_*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["crypticwisdom.pythonanywhere.com", "127.0.0.1", "localhost"]

# MySQL PythonAnywhere database settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'crypticwisdom$techies_jobs',
#         'USER': 'crypticwisdom',
#         'HOST': 'crypticwisdom.mysql.pythonanywhere-services.com',
#         'PORT': '3306',
#         'PASSWORD': 'iamherenow',
#     }
# }

# MySQL Local database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'techies_db',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'PASSWORD': 'iamherenow',
    }
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer', "Token"),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
    "http://127.0.0.1",
    'https://techies-jobs.vercel.app'
]