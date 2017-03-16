from .base import *

ALLOWED_HOSTS = ["api.sonical.ardent.tech"]

CORS_ORIGIN_WHITELIST = ('sonical.ardent.tech',)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_env_var('SONICAL_EMAIL_HOST')
EMAIL_HOST_PASSWORD = get_env_var('SONICAL_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = get_env_var('SONICAL_EMAIL_HOST_USER')

MEDIA_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'static')
STATIC_URL = '/static/'
