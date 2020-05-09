import re
from time import time
from typing import Any, Dict, List, Optional

from flask import current_app, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from .. import db
from ..models.playlists import (
    CumulativePlaylist,
    MonthlyPlaylist,
    Playlist,
    YearlyPlaylist,
)
from .auth import current_user

SPOTIFY_SCOPES = [
    "user-read-playback-state",
    "playlist-modify-private",
    "playlist-read-private",
]

MONTHLY_REGEX = re.compile(r"^Favourite Songs - (?P<month>[\w ]+) (?P<year>\d+)$")
YEARLY_REGEX = re.compile(r"^Favourite Songs - (?P<year>\d+)$")


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


def get_all_objects(
    initial_results: Dict[str, Any], spotify_client: Spotify
) -> List[Any]:
    results = initial_results
    objects = results["items"]

    while results["next"] is not None:
        results = Spotify.next(objects["next"])
        objects.extend(results["items"])

    return objects


# TODO: Make this a semi-automated process, with user input
# This is for testing purposes
def import_playlists() -> List[Dict[str, Any]]:
    if current_user is None:
        raise RuntimeError(
            "Playlists can only be imported with a currently logged in user"
        )

    spotify_client = get_spotify_client()
    if spotify_client is None:
        raise RuntimeError("Unable to retrieve Spotify client for current user")

    user_playlists = get_all_objects(
        spotify_client.current_user_playlists(), spotify_client
    )

    new_playlists = []

    for playlist in user_playlists:
        if Playlist.get_by_spotify_id(playlist["id"]) is not None:
            continue
        monthly_match = MONTHLY_REGEX.match(playlist["name"])
        yearly_match = YEARLY_REGEX.match(playlist["name"])
        playlist_kwargs = {
            "spotify_id": playlist["id"],
            "name": playlist["name"],
            "owner_id": current_user.id,
        }
        if monthly_match:
            db.session.add(
                MonthlyPlaylist(
                    **playlist_kwargs,
                    month=monthly_match["month"],
                    year=monthly_match["year"]
                )
            )
        elif yearly_match:
            db.session.add(YearlyPlaylist(**playlist_kwargs, year=yearly_match["year"]))
        elif playlist["name"] == "Favourite Songs":
            db.session.add(CumulativePlaylist(**playlist_kwargs))
        else:
            continue

        new_playlists.append(playlist)

    db.session.commit()

    return new_playlists
