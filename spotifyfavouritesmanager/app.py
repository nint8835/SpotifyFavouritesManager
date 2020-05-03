import os

from dotenv import load_dotenv
from flask import Flask
from flask_dance.contrib.spotify import make_spotify_blueprint

from . import alembic, db
from .views.auth import auth_api

app = Flask(__name__)
load_dotenv()
app.config.from_object(
    f"spotifyfavouritesmanager.config.{os.environ.get('FLASK_CONFIG','DEVELOPMENT')}"
)
db.init_app(app)
alembic.init_app(app)

app.register_blueprint(auth_api)

spotify_blueprint = make_spotify_blueprint(
    client_id=app.config["SPOTIFY_CLIENT_ID"],
    client_secret=app.config["SPOTIFY_CLIENT_SECRET"],
)
app.register_blueprint(spotify_blueprint, prefix="/oauth")
