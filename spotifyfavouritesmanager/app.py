import os

from flask import Flask

from . import alembic, db
from .views.auth import auth_api

app = Flask(__name__)
app.config.from_object(
    f"spotifyfavouritesmanager.config.{os.environ.get('FLASK_CONFIG','DEVELOPMENT')}"
)
db.init_app(app)
alembic.init_app(app)

app.register_blueprint(auth_api)
