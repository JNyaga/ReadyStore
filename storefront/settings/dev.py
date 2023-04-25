from .common import *
import dj_database_url

DEBUG = True

SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'


# db_config = dj_database_url.parse(env('DATABASE_URL'))
# # db_config['ATOMIC_REQUESTS'] = True

# DATABASES = {
#     'default': db_config,
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': env('DATABASE_PASSWORD')
    }
}
