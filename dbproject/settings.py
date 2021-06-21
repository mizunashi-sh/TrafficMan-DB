"""
Django settings for dbproject project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TrafficMan',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dbproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dbproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLEUI_CONFIG={
    'menus': [
        {
            'app': 'TrafficMan',
            'name': '快捷查询',
            'icon': 'far fa-map',
            'models': [
                {
                    'name': '机动车-车主信息联合查询',
                    'url': 'TrafficMan/ownervehicleview/',
                    'icon': 'fas fa-search',
                },
                {
                    'name': '未处理违章查询',
                    'url': 'TrafficMan/unprocessedviolationview/',
                    'icon': 'fas fa-search',
                },
                {
                    'name': '逾期违章查询',
                    'url': 'TrafficMan/exceededviolationview/',
                    'icon': 'fas fa-search',
                },
            ]
        },
        {
            'app': 'TrafficMan',
            'name': '信息管理/查询',
            'icon': 'fas fa-cog',
            'models': [
                {
                    'name': '驾驶员/车主信息管理',
                    'url': 'TrafficMan/userprofile/',
                    'icon':'far fa-address-card',
                },
                {
                    'name': '机动车信息管理',
                    'url': 'TrafficMan/vehicle',
                    'icon': 'fas fa-car',
                },
                {
                    'name': '违章信息管理',
                    'url': 'TrafficMan/violation/',
                    'icon': 'far fa-list-alt',
                },
                {
                    'name': '违章处理记录查询',
                    'url': 'TrafficMan/violationprocessrecordview',
                    'icon': 'fas fa-search',
                }
            ]
        },
        {
            'app': 'auth',
            'name': '认证与授权',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '组',
                    'icon': 'fas fa-users-cog',
                    'url': 'auth/group/'
                }
            ]
        }
    ]
}

SIMPLEUI_HOME_INFO = False
SIMPLEUI_LOGIN_PARTICLES = False
SIMPLEUI_LOGO = 'https://i.loli.net/2021/05/30/VUh1RHeApbnBZOa.png'