from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'changeme'
DEBUG = True

ALLOWED_HOSTS = []

TABBED_ADMIN_USE_JQUERY_UI = True

INSTALLED_APPS = [
    'cmdb',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'tabbed_admin',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ]
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'cmdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTHENTICATION_BACKENDS = (
    'suap_backend.backends.SuapOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SESSION_COOKIE_NAME = 'sti-cmdb'
LOGIN_REDIRECT_URL = '/accounts/profile/'

SOCIAL_AUTH_SUAP_KEY = 'Jga8poWzWReVrBEfOOjuevEwVAN6yr5LIA8oPqdg'
SOCIAL_AUTH_SUAP_SECRET = 'e9vHaRMg5Tb4g95Y8fwN2gRs8o0kfXuEVyi0KHsHc7h1E9bzZGxmL3KYFdhxOt6D0gf9u8d6ITvRUtsVhL8FolIjp0GXCIXcmpBmOwIfTfwXGCcjUm9qYnYDpIJEdbrA'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'