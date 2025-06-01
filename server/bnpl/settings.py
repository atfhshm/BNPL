from datetime import timedelta
from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / '.env')


DEBUG: bool = env('DEBUG', cast=bool, default=True)
SECRET_KEY: str = env('SECRET_KEY')
ALLOWED_HOSTS: list[str] = env.list('ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS: list[str] = env.list('CSRF_TRUSTED_ORIGINS')

# CORS settings
CORS_ALLOW_ALL_ORIGINS: bool = env('CORS_ALLOW_ALL_ORIGINS', cast=bool, default=True)
CORS_ALLOW_CREDENTIALS: bool = env('CORS_ALLOW_CREDENTIALS', cast=bool, default=True)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'silk',
    'rest_framework',
    'corsheaders',
    'phonenumber_field',
    'django_celery_beat',
    'django_celery_results',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'djmoney',
    # local
    'apps.user.apps.UserConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.installment.apps.InstallmentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third party
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'bnpl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bnpl.wsgi.application'
ASGI_APPLICATION = 'bnpl.asgi.application'
APPEND_SLASH = True


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Redis
REDIS_URL: str = env('REDIS_URL', cast=str, default='redis://redis:6379')

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# Celery
CELERY_BROKER_URL: str = REDIS_URL
CELERY_RESULT_BACKEND: str = REDIS_URL
CELERY_ACCEPT_CONTENT: list[str] = ['application/json']
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_TIMEZONE: str = 'UTC'
CELERY_TASK_TRACK_STARTED: bool = True
CELERY_TASK_TIME_LIMIT: int = 30 * 60

CELERY_BEAT_SCHEDULER: str = 'django_celery_beat.schedulers.DatabaseScheduler'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILE_DIR = BASE_DIR / 'static/'
STATICFILES_DIRS = (STATICFILE_DIR,)


STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = BASE_DIR.joinpath('staticfiles/')
MEDIA_ROOT = MEDIA_ROOT = BASE_DIR.joinpath('uploads/')

# Default primary key field type and user model

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'bnpl.exception_handlers.server_error_handler',
}

ACCESS_TOKEN_EXPIRY_MINUTES = env('ACCESS_TOKEN_EXPIRY_MINUTES', cast=int)
REFRESH_TOKEN_EXPIRY_DAYS = env('REFRESH_TOKEN_EXPIRY_DAYS', cast=int)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'BNPL server API',
    'DESCRIPTION': 'BNPL API schema and documentation.',
    'VERSION': '0.1.0',
    'CONTACT': {
        'name': 'Atef hesham',
        'url': 'https://atfhshm.com',
        'email': 'atefheshamattia@gmail.com',
    },
    'SERVE_INCLUDE_SCHEMA': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'POSTPROCESSING_HOOKS': [],
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}
