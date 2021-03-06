from typing import Any

from flask import Blueprint, jsonify

from ..utils.auth import login_required
from ..utils.spotify import get_spotify_client, import_playlists

testing_api = Blueprint("testing", __name__)


@testing_api.route("/now_playing")
@login_required()
def now_playing() -> Any:
    client = get_spotify_client()
    if client is None:
        return jsonify(nope=True), 418

    return jsonify(track=client.current_user_playing_track())


@testing_api.route("/import")
@login_required()
def test_import_playlists() -> Any:
    return jsonify(imported=[playlist["name"] for playlist in import_playlists()])
