import os

class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///journal_club.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
