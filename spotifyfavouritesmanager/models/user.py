from typing import Optional, Type

from .. import db
from ..utils.types import TokenDetails


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    token_data = db.Column(db.JSON, nullable=False)

    @classmethod
    def add(
        cls: Type["User"],
        username: str,
        token_data: Optional[TokenDetails] = None,
        *,
        commit: bool = False
    ) -> "User":
        instance = cls(username=username, token_data=token_data)
        db.session.add(instance)

        if commit:
            db.session.commit()

        return instance

    @classmethod
    def get_by_username(cls: Type["User"], username: str) -> Optional["User"]:
        return cls.query.filter_by(username=username).first()
