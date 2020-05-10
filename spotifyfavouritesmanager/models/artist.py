from typing import Optional, Type

from .. import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    @classmethod
    def get_by_spotify_id(cls: Type["Artist"], spotify_id: str) -> Optional["Artist"]:
        return cls.query.filter_by(spotify_id=spotify_id).first()
