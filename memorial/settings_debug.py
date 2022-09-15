from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-t#p_8r9#ygue45)vn&ob%z@)oza^d2(@o0t1*&0@4#2(rfzq^o'
ALLOWED_HOSTS = ["*"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}