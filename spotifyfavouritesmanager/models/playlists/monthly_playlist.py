from ... import db
from .playlist import Playlist


class MonthlyPlaylist(Playlist):
    id = db.Column(db.Integer, db.ForeignKey("playlist.id"), primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "monthly_playlist"}
