"""
Django settings for foodsystem project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)r71_%rvsznv^$f#z*ct64*k^ttk%!r#)-w2@d4o^9gj8(wy#d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 1.允许的主机
ALLOWED_HOSTS = ['*']


# Application definition
# 2.注册
INSTALLED_APPS = [
    'simpleui',  # 后台管理系统界面框架
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # 接口协议
    'tinymce',  # 注册富文本应用
    'user',  # 美食推荐系统，就是自定义应用
]
# 3.中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # 增加缓存中间件
]

ROOT_URLCONF = 'foodsystem.urls'

# 4.模板文件路径
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 增加模板文件信息
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

WSGI_APPLICATION = 'foodsystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# 5.配置数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 修改数据库为mysql
        'NAME': 'foodsystem',   # 数据库名称，注意后续创建数据库的名字需要跟这个名字一样
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库的密码
        'HOST': '127.0.0.1',  # 主机IP地址
        'PORT': 3306,  # 数据库端口号
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
# 6.国际化配置
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# 7.静态文件配置
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # 静态文件的文件夹
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),] # 静态文件的文件夹
STATIC_URL = '/static/'  # 静态文件的路径，默认已经有了
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 媒体文件的文件夹
MEDIA_URL = '/media/'  # 媒体文件的路径

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 8.作用于管理后台中的富文本编辑器配置，写在最后面就可以了
TINYMCE_DEFAULT_CONFIG = {
    # 使用高级主题,备选项还有简单主题
    'theme': 'advanced',
    # 'theme': 'simple',
    # 必须指定富文本编辑器(RTF=rich text format)的宽高
    'width': 800,
    'height': 600,
    # 汉化
    'language': 'zh',
    # 自定义常用的固定样式
    'style_formats': [
        # title=样式名称
        # styles=自定义css样式
        # inline:xxx = 将加样式后的文本放在行内元素中显示
        # block:xxx = 将加样式后的文本放在块级元素中显示
        {'title': 'Bold text', 'inline': 'b'},
        {'title': 'Red text', 'inline': 'span', 'styles': {'color': '#ff0000'}},
        {'title': 'Red header', 'block': 'h1', 'styles': {'color': '#ff0000'}},
        {'title': 'Example 1', 'inline': 'span', 'classes': 'example1'},
        {'title': 'Example 2', 'inline': 'span', 'classes': 'example2'},
        {'title': 'Table styles'},
        {'title': 'Table row 1', 'selector': 'tr', 'classes': 'tablerow1'}
    ],
}

SIMPLEUI_HOME_INFO = False  # 页面左侧信息是否展示
SIMPLEUI_DEFAULT_ICON = False  # 是否展示默认图标
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'dynamic': True,
    'menu_display': ['用户模块', '认证和授权'],
    'menus': [
        {
            'name': '用户模块',
            'icon': 'fa fa-address-food',
            'models': [
                {
                    'name': '美食信息',
                    'icon': 'fa fa-info-circle',
                    'url': 'user/food/'
                },
                {
                    'name': '数据统计',
                    'icon': 'fa fa-building',
                    'url': 'user/num/'
                },
                {
                    'name': '菜系信息',
                    'icon': 'fa fa-bars',
                    'url': 'user/tags/'
                },
                {
                    'name': '用户信息',
                    'icon': 'fa fa-server',
                    'url': 'user/user/'
                },
                {
                    'name': '留言信息',
                    'icon': 'fa fa-braille',
                    'url': 'user/messageboard/'
                },
                {
                    'name': '评论信息',
                    'icon': 'fa fa-bookmark',
                    'url': 'user/comment/'
                },
                {
                    'name': '评分信息',
                    'icon': 'fa fa-bell',
                    'url': 'user/rate/'
                },
                {
                    'name': '论坛信息',
                    'icon': 'fa fa-comments',
                    'url': 'user/collectboard/'
                }
            ]
        },
        {
            'name': '认证和授权',
            'icon': 'fas fa-shield-alt',
            'models': [
                {
                    'name': '用户',
                    'icon': 'far fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '组',
                    'icon': 'fas fa-users-cog',
                    'url': 'auth/group/'
                },
            ]
        }
    ]
}