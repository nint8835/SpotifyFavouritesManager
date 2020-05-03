import logging
from typing import Any

from flask import Blueprint, jsonify, redirect, session, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.spotify import spotify

from .. import db
from ..models.user import User
from ..utils.types import TokenDetails

logger = logging.getLogger(__name__)

auth_api = Blueprint("auth", __name__)


@auth_api.route("/")
def auth_begin_route() -> Any:
    if "spotify_username" not in session:
        return redirect(url_for("spotify.login"))
    else:
        current_user = User.get_by_username(session["spotify_username"])
        if current_user is None:
            return redirect(url_for("spotify.login"))
        return jsonify(username=current_user.username, token=current_user.token_data)


@oauth_authorized.connect
def logged_in(blueprint: Blueprint, token: TokenDetails) -> None:
    logger.info(token)
    user_details = spotify.get("/v1/me").json()
    username = user_details["id"]

    user = User.get_by_username(username)
    if user is None:
        user = User.add(username=username)

    user.token_data = token

    session["spotify_username"] = username
    db.session.commit()
