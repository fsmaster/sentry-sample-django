import os
from pathlib import Path

import sentry_sdk

# This is the whole Sentry setup. DjangoIntegration is switched on by itself
# when sentry-sdk sees Django installed.
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("SENTRY_ENVIRONMENT", "local"),
    release=os.environ.get("RELEASE", "sample-django@dev"),
    send_default_pii=False,
    traces_sample_rate=1.0,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "only-for-the-sample")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth"]
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "shop.urls"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
USE_TZ = True
