from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from . import models, forms, views, error_handlers, api_views
