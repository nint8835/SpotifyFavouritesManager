import logging
from typing import Any

from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

auth_api = Blueprint("auth", __name__)


@auth_api.route("/auth")
def auth_begin_route() -> Any:
    return jsonify(test=True)
