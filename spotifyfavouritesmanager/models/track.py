from typing import Optional, Type

from .. import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    artist = db.relationship("Artist")

    @classmethod
    def get_by_spotify_id(cls: Type["Track"], spotify_id: str) -> Optional["Track"]:
        return cls.query.filter_by(spotify_id=spotify_id).first()
