from .settings_common import *

# DEBUG = True
DEBUG = False
ALLOWED_HOSTS = ['*']

# 開発時はアプリから送信されるメールの内容を terminal に出力。
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
