"""
Django settings for zh project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+h^-mr^x0v(4@_p0=c+2z^6yv9+y^2g&fd32k+dr2j&9ifi8m*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ACCOUNT_ALLOW_REGISTRATION = True

ACCOUNT_AUTHENTICATION_METHOD = "username_email" # 用户登录的方式可以为 username_email

ACCOUNT_EMAIL_REQUIRED = True  # 是否要求邮箱信息

ACCOUNT_EMAIL_VERIFICATION = "none" # 是否验证邮件 #mandatory（强制），optional（可选），none（不要）

ACCOUNT_ADAPTER = "users.adapters.AccountAdapter"

SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"


# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "mikuwithyou@163.com"
EMAIL_HOST_PASSWORD = "QAZ759926"        # 这个不是邮箱密码，而是授权码
EMAIL_USE_SSL = True                    # 这里必须是 True，否则发送不成功
EMAIL_FROM = "mikuwithyou@163.com"         # 发件人
DEFAULT_FROM_EMAIL = "Miku 测试 <mikuwithyou@163.com>"  # 默认发件人(如果不添加DEFAULT_FROM_EMAIL字段可能会导致如下错误: 451, b'Sender address format error.', 'webmaster@localhost')

ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'users',
    'news',
    'articles',
    'django.contrib.sites',
    'allauth', # allauth包
    'allauth.account', # 本地的allauth认证
    'allauth.socialaccount', # 第三方的账号认证
    'sorl.thumbnail',
    'crispy_forms',
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'allauth.socialaccount.providers.baidu',
    'taggit',
    'markdownx',
    'django.forms',
    'django_comments',

]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
MARKDOWNX_SERVER_CALL_LATENCY = 1000
# alluth 相关设置
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # django admin所使用的用户登录与django-allauth无关
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth 身份验证
]

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "home"  # 登陆跳转设置
ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"
LOGIN_URL = "account_login"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'zh.wsgi.application'



# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zh',  # 数据库的名字
        'USER': 'root',  # 连接数据库的用户
        'PASSWORD': 'miku039',  # 密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

# app django.contrib.sites需要的设置
SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'nginx')  # BASE_DIR 是项目的绝对地址

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)



MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')