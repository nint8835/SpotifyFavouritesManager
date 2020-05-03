import os


class COMMON:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


class DEVELOPMENT(COMMON):
    SQLALCHEMY_DATABASE_URI = "postgresql://sfm:password@localhost:5432/sfm_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "this key isn't secret"
