import os

DEBUG = True

MAIL_SENDER = ('BRUTUS', 'decave12357@gmail.com')
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'decave12357@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

MONGO_URI = "mongodb://localhost:27017/my_database_2"
