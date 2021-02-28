import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = False
# Enable debug mode.
DEBUG = True

# Connect to the database

# Add connection to the localhost postgres db environmental variable
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False