from .common import *
import os
import dj_database_url


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['readystore.onrender.com']

db_config = dj_database_url.parse(env('DATABASE_URL'))
# db_config['ATOMIC_REQUESTS'] = True

DATABASES = {
    'default': db_config,
}
