import logging
from typing import Any

from flask import Blueprint, jsonify, session
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.spotify import spotify
from flask_jwt_extended import create_access_token

from .. import db
from ..models.user import User
from ..utils.auth import current_user, login_required
from ..utils.types import TokenDetails

logger = logging.getLogger(__name__)

auth_api = Blueprint("auth", __name__)


@auth_api.route("/")
@login_required(should_redirect=True)
def index_route() -> Any:
    return jsonify(username=current_user.username)


@auth_api.route("/jwt")
@login_required()
def generate_jwt() -> Any:
    return jsonify(token=create_access_token(identity=current_user.username))


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
