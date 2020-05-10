import logging
import re
from time import time
from typing import Any, Dict, List, Optional

from flask import current_app, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from .. import db
from ..models import Artist, Track
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

logger = logging.getLogger(__name__)


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
        results = spotify_client.next(results)
        objects.extend(results["items"])

    return objects


# TODO: Make this like an actual good bit of code
def import_playlist_contents(playlist: Playlist, client: Spotify) -> None:
    logger.info(f"Importing contents for playlist {playlist.name}")
    tracks = get_all_objects(client.playlist_tracks(playlist.spotify_id), client,)
    for track in tracks:
        track = track["track"]
        logger.info(f"Adding track {track['name']}")
        track_object = Track.get_by_spotify_id(track["id"])
        if track_object is None:
            logger.info("Track doesn't exist, creating")
            track_object = Track(spotify_id=track["id"], name=track["name"])

            for artist in track["artists"]:
                artist_obj = Artist.get_by_spotify_id(artist["id"])
                if artist_obj is None:
                    logger.info(
                        f"Artist {artist['name']} for track does not exist, creating"
                    )
                    artist_obj = Artist(spotify_id=artist["id"], name=artist["name"])
                    db.session.add(artist_obj)
                track_object.artists.append(artist_obj)
            db.session.add(track_object)
        playlist.tracks.append(track_object)
    logger.info("Playlist contents imported")
    db.session.commit()


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
    new_playlist_objs = []

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
        new_playlist_obj = None
        if monthly_match:
            new_playlist_obj = MonthlyPlaylist(
                **playlist_kwargs,
                month=monthly_match["month"],
                year=monthly_match["year"],
            )

        elif yearly_match:
            new_playlist_obj = YearlyPlaylist(
                **playlist_kwargs, year=yearly_match["year"]
            )
        elif playlist["name"] == "Favourite Songs":
            new_playlist_obj = CumulativePlaylist(**playlist_kwargs)
        else:
            continue

        db.session.add(new_playlist_obj)
        new_playlists.append(playlist)
        new_playlist_objs.append(new_playlist_obj)

    for new_playlist in new_playlist_objs:
        import_playlist_contents(new_playlist, spotify_client)

    db.session.commit()

    return new_playlists
