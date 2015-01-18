import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DEBUG = True
SECRET_KEY = '7$gkoy@rr#sok+gq780grpl1^g7c=o#h#(gxy5_p9dtut%oiyr'

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'pipeline',

    'noetikon.files',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'noetikon.urls'
WSGI_APPLICATION = 'noetikon.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../uploads')
MEDIA_URL = '/uploads/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates'),

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# PIPELINE_COMPILERS = 'pipeline.compilers.sass.SASSCompiler',
#
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'pipeline.finders.PipelineFinder',
# )
#
# PIPELINE_CSS = {
#     'main': {
#         'source_filenames': (
#             'sass/main.sass',
#         ),
#         'output_filename': 'sass/main.css',
#     },
# }
#
