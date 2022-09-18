from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the  secret key used in production secret!
SECRET_KEY = 'django-insecure-s5c49@t8bw*n16rw_f#im(e_i!xbm7%3%y*qq(lk@==ozy2c1h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'account',
    'blog',
    'coment',
    'appblog',
    'taggit',
    'django_social_share',
    'django.contrib.gis',
    'crispy_forms',
    'mdeditor',
    'azbankgateways',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'shop/blog/templates')],
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

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sqlshop',
        'USER': 'postgres',
        'PASSWORD': 'demodomo',
        'HOST': 'localhost',
        'PORT': 5432 ,
        'ENGINE': 'django.contrib.gis.db.backends.postgis', 
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

POSTGIS_VERSION = (2, 4, 3)
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR , 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'account.User'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'demodomone@gmail.com'
DEFAULT_FORM_EMAIL = 'demodomone@gmail.com'
EMAIL_HOST_PASSWORD = 'moxczeohuhgyowqm'



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.name == 'nt':
    VIRTUAL_ENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']

AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
    #    'BMI': {
    #        'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
    #        'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
    #        'SECRET_KEY': '<YOUR SECRET CODE>',
    #    },
       'SEP': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
       },
    #    'ZARINPAL': {
    #        'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
    #        'SANDBOX': 0,  # 0 disable, 1 active
    #    },
    #    'IDPAY': {
    #        'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
    #        'METHOD': 'POST',  # GET or POST
    #        'X_SANDBOX': 0,  # 0 disable, 1 active
    #    },
    #    'ZIBAL': {
    #        'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
    #    },
    #    'BAHAMTA': {
    #        'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
    #    },
    #    'MELLAT': {
    #        'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
    #        'USERNAME': '<YOUR USERNAME>',
    #        'PASSWORD': '<YOUR PASSWORD>',
    #    },
   },
   'IS_SAMPLE_FORM_ENABLE': True, # اختیاری و پیش فرض غیر فعال است
   'DEFAULT': 'SEP',
   'CURRENCY': 'IRR', # اختیاری
   'TRACKING_CODE_QUERY_PARAM': 'tc', # اختیاری
   'TRACKING_CODE_LENGTH': 16, # اختیاری
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', # اختیاری
   'BANK_PRIORITIES': [
    #    'BMI',
       'SEP',
       # and so on ...
   ], # اختیاری
}

# https
# don't remove
# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = 'SAMEORIGIN' 

MDEDITOR_CONFIGS = {
    'default':{
        'width': '90% ',  # Custom edit box width
        'height': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar 
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True, # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'zh'  # zh / en / es 
    }
    
}