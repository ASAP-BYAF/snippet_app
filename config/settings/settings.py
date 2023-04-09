from .settings_common import *

#DEBUG = False
DEBUG = True
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

AWS_SES_ACCESS_KEY_ID=os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY=os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
EMAIL_BACKEND='django_ses.SESBackend'
AWS_SES_REGION_NAME='eu-north-1'
AWS_SES_REGION_ENDPOINT='email.eu-north-1.amazonaws.com'

STATIC_ROOT = '/var/www/html/static'
