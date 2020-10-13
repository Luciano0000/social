
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dgdsxu!l)#i6n)92q0_wix%jz!e*n6y@#ht#8ghvi1)p3z-c3j'

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
    'App',
    'social',
    'vip',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.AuthMiddleware',
    'common.middleware.LogicErrorMiddleware',
]

ROOT_URLCONF = 'fuck.urls'

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

WSGI_APPLICATION = 'fuck.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

CACHES = {
    "default":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS":{
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION":-1,
            "PASSWORD": "123",
        }
    }
}
REDIS = {
    'Master':{
        'host':'127.0.0.1',
        'port':6379,
        'db':1,
        'password':'123'
    },
    'Slave':{
        'host':'127.0.0.1',
        'port':6379,
        'db':1,
        'password':'123'
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "fuck",
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'POST': '3306',
    },
    'sec_db1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "tar_fuck1",
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'POST': '3306',
    },
    'sec_db2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "tar_fuck2",
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'POST': '3306',
    }

}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = 'medias'

LOGGING = {
    'version':1,
    'disable_existing_loggers':True,
    # 格式配置
    'formatters':{
        'simple':{
            'format':'%(asctime)s %(module)s.%(funcName)s:%(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S',

        },
        'verbose':{
            'format':('%(asctime)s %(levelname)s [%(process)d-%(threadName)s]'
                      '%(module)s.%(funcName)s line %(lineno)d:%(message)s'
                      ),
            'datefmt':'%Y-%m-%d %H:%M%S',
        }
    },
    #Handler　配置
    'handlers':{
        'console':{
            'class':'logging.StreamHandler',
            'level':'DEBUG' if DEBUG else 'WARNING'
        },
        'info':{
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/logs/info.log'.format(BASE_DIR),# 日志保存路径
            'when':'D', #每天切割日志
            'backupCount':30,#日志保留30天
            'formatter':'simple',
            'level':'INFO',
        },
        'error':{
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/logs/error.log'.format(BASE_DIR),
            'when':'W0',
            'backupCount':4,
            'formatter':'verbose',
            'level':'WARNING',
        }
    },

    # logger配置
    'loggers':{
        'django':{
            'handlers':['console'],

        },
        'inf':{
            'handlers':['info'],
            'propagate':True,
            'level':'INFO',
        },
        'err':{
            'handlers':['error'],
            'propagate':True,
            'level':'WARNING',
        }
    }


}
