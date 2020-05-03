from time import time
from typing import Optional

from flask import current_app, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from .. import db
from .auth import current_user

SPOTIFY_SCOPES = [
    "user-read-playback-state",
    "playlist-modify-private",
    "playlist-read-private",
]


def get_fresh_token() -> Optional[str]:
    if current_user is None:
        return None

    token_data = current_user.token_data

    if token_data["expires_at"] - int(time()) < 60:
        spotify_oauth = SpotifyOAuth(
            client_id=current_app.config["SPOTIFY_CLIENT_ID"],
            client_secret=current_app.config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=url_for("spotify.authorized", external=True),
            scope=",".join(SPOTIFY_SCOPES),
        )
        token_data = spotify_oauth.refresh_access_token(token_data["refresh_token"])
        current_user.token_data = token_data
        db.session.commit()
    return token_data["access_token"]


def get_spotify_client() -> Optional[Spotify]:
    token = get_fresh_token()
    if token is None:
        return None

    return Spotify(auth=token)
