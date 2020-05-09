from ... import db
from .playlist import Playlist


class CumulativePlaylist(Playlist):
    id = db.Column(db.Integer, db.ForeignKey("playlist.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "cumulative_playlist"}
