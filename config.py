import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://flasktest:Password1!@localhost:5432/fl_test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
