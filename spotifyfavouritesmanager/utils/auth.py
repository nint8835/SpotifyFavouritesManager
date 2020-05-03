from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from flask import jsonify, redirect, session, url_for
from werkzeug.local import LocalProxy

from ..models.user import User

current_user: Optional[User] = cast(
    Optional[User],
    LocalProxy(lambda: User.get_by_username(session.get("spotify_username"))),
)


def _generate_login_error_response(should_redirect: bool) -> Any:
    if should_redirect:
        return redirect(url_for("spotify.login"))
    else:
        return jsonify(message="You are not logged in."), 401


F = TypeVar("F", bound=Callable[..., Any])


def login_required(should_redirect: bool = False) -> Callable[[F], F]:
    def outer_wrapper(func: F) -> F:
        @wraps(func)
        def inner_wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            if "spotify_username" not in session:
                return _generate_login_error_response(should_redirect)
            current_user = User.get_by_username(session["spotify_username"])
            if current_user is None:
                return _generate_login_error_response(should_redirect)
            return func(*args, **kwargs)

        return cast(F, inner_wrapper)

    return outer_wrapper
