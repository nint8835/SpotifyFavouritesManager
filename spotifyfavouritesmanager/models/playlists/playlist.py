from typing import Optional, Type

from ... import db

TRACKS_TABLE = db.Table(
    "playlist_tracks",
    db.Column("track_id", db.Integer, db.ForeignKey("track.id"), primary_key=True),
    db.Column(
        "playlist_id", db.Integer, db.ForeignKey("playlist.id"), primary_key=True
    ),
)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    playlist_type = db.Column(db.Text, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User")

    tracks = db.relationship(
        "Track",
        secondary=TRACKS_TABLE,
        lazy="subquery",
        backref=db.backref("tracks", lazy=True),
    )

    __mapper_args__ = {
        "polymorphic_identity": "playlist",
        "polymorphic_on": playlist_type,
    }

    @classmethod
    def get_by_spotify_id(
        cls: Type["Playlist"], spotify_id: str
    ) -> Optional["Playlist"]:
        return cls.query.filter_by(spotify_id=spotify_id).first()
