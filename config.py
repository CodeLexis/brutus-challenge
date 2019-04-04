import os

DEBUG = True

LOGIN_REST_PERIOD_MINUTES = 5
LOGIN_REST_PERIOD_SECONDS = 5 * 60
MAIL_SENDER = ('BRUTUS', 'decave12357@gmail.com')
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'decave12357@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAX_LOGIN_ATTEMPTS = 3
MONGO_URI = "mongodb://localhost:27017/my_database_2"
