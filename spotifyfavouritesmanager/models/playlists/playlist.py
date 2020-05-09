from ... import db


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    playlist_type = db.Column(db.Text, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User")

    __mapper_args__ = {
        "polymorphic_identity": "playlist",
        "polymorphic_on": playlist_type,
    }
