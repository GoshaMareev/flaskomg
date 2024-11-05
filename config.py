import os

class Config:
    # Update the connection string to match your PostgreSQL setup
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://flasktest:Password1!@localhost:5432/fl_test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
