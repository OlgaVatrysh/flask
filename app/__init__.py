import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'secret-key'
app.database_url = 'app.db'

from app import routes