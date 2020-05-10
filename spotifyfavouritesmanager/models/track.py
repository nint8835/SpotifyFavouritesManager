from typing import Optional, Type

from .. import db

ARTISTS_TABLE = db.Table(
    "track_artists",
    db.Column("track_id", db.Integer, db.ForeignKey("track.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id"), primary_key=True),
)


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)

    artists = db.relationship(
        "Artist",
        secondary=ARTISTS_TABLE,
        lazy="subquery",
        backref=db.backref("tracks", lazy=True),
    )

    @classmethod
    def get_by_spotify_id(cls: Type["Track"], spotify_id: str) -> Optional["Track"]:
        return cls.query.filter_by(spotify_id=spotify_id).first()
