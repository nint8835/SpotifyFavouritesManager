from ... import db
from .playlist import Playlist


class YearlyPlaylist(Playlist):
    id = db.Column(db.Integer, db.ForeignKey("playlist.id"), primary_key=True)
    year = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "yearly_playlist"}
