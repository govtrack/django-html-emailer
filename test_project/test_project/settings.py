import os, random, string

INSTALLED_APPS = [
    "htmlemailer",
    "test_project"
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "".join([random.choice(getattr(string, 'letters', string.ascii_letters)) for _ in range(50)])
DEBUG = True
ROOT_URLCONF = 'test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'test_project.wsgi.application'

