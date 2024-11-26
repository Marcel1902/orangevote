import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%eg+ckh^7t)e*r=pdz)3=h&o#g8*6ox!@yh$@1@!oxtyg_j@4q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vote',
]

JAZZMIN_SETTINGS = {
    # Nom et sous-titre
    "site_title": "ORANGE VOTE Admin",
    "site_header": "Admin VOTE",
    "welcome_sign": "Bienvenue sur l'administration du VOTE",

    # Personnalisation du menu
    "custom_links": {
        "app_label": [{
            "name": "Statistiques",
            "url": "custom-stats-view",
            "icon": "fas fa-chart-line",
        }],
    },

    # Icônes pour les modèles
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "vote.Commune": "fas fa-plane",
        "vote.Vote": "fas fa-vote-yea",
        "vote.Image": "fas fa-poll",
    },

    # Interface utilisateur
    "show_ui_builder": True,  # Permet de modifier l'UI à la volée
    "navigation_expanded": True,  # Toujours afficher le menu complet
    "order_with_respect_to": ["auth", "vote"],  # Ordre des applications
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orangevote.urls'

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

WSGI_APPLICATION = 'orangevote.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Si vous souhaitez utiliser un dossier "images" dans static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Chemin où les fichiers médias seront stockés
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL pour accéder aux fichiers médias
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
