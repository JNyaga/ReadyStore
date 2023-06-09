import environ
from datetime import timedelta
import os
from pathlib import Path
from celery.schedules import crontab
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env()

environ.Env.read_env()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'djoser',
    'silk',
    'django_extensions',
    'cloudinary',
    'cloudinary_storage',
    'playground',
    'debug_toolbar',
    'store',
    'tags',
    'likes',
    'core',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# if DEBUG:
#     MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8001',
    'http://127.0.0.1:8001',
]

ROOT_URLCONF = 'storefront.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storefront.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# define new object for Django Rest Framework
# this prevents the default behaviour to display strings instead of numbers in the API
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated'
    # ]
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT',),
}

# Tell django to use the core user instead of the original for authentication
AUTH_USER_MODEL = 'core.User'

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password-reset/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'from@joelreadysell.com'


ADMINS = [
    ('John', 'admin@readysell.com'),
]


# Celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
# CELERY_RESULT_BACKEND = "localhost:6379"
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        # 'schedule':crontab(day_of_week=1, hour=7, minute=30)
        'schedule': 5,
        'args': ['Hello World'],
        # 'kwargs':{}
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": 10*60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


GRAPH_MODELS = {
    # 'all_applications': True,
    'app_labels': ["store"],
    'group_models': True,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'verbose'
        }
    },

    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO')
        }
    },

    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'
        }
    }
}


# cloudinary
# cloudinary.config(
#     cloud_name=env('CLOUDINARY_NAME'),
#     api_key=env('CLOUDINARY_API_KEY'),
#     api_secret=env('CLOUDINARY_API_SECRET'))

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}
