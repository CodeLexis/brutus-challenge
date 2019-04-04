from datetime import datetime

from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash

from app import app


client = PyMongo(app)
db = client.db.interview


class LoginActivity(object):
    created_at = None
    email = None
    ip_address = None
    status = None

    def __init__(self, **kwargs):
        self.created_at = datetime.now()
        self.email = kwargs['email']
        self.ip_address = kwargs['ip_address']
        self.status = kwargs['status']

    @property
    def data(self):
        return {
            'created_at': self.created_at,
            'email': self.email,
            'ip_address': self.ip_address,
            'status': self.status
        }

    def save(self):
        db.login_activities.insert_one(self.data)

    @staticmethod
    def find(kw):
        return db.login_activities.find_one(kw)


class User(object):
    first_name = None
    last_name = None
    email = None
    password = None

    def __init__(self, hash_password=True, **kwargs):
        self.fullname = kwargs['fullname']
        self.email = kwargs['email']

        if hash_password:
            self.password = self.hash_password(kwargs['password'])
        else:
            self.password = kwargs['password']

    def hash_password(self, text):
        return generate_password_hash(text)

    def verify_password(self, text):
        return check_password_hash(self.password, text)

    @property
    def data(self):
        return {
            'fullname': self.fullname,
            'email': self.email,
            'password': self.password
        }

    def save(self):
        db.users.insert_one(self.data)

    @staticmethod
    def find(kw):
        data = db.users.find_one(kw)

        if data:
            return User(hash_password=False, **data)
