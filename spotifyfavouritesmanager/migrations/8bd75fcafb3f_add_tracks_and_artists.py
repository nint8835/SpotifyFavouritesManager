"""Add tracks and artists

Revision ID: 8bd75fcafb3f
Revises: 15e1723f01c6
Create Date: 2020-05-09 23:50:05.490279

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bd75fcafb3f"
down_revision = "15e1723f01c6"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.create_table(
        "artist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("spotify_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "track",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("spotify_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("artist_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["artist_id"], ["artist.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playlist_tracks",
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("playlist_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["playlist_id"], ["playlist.id"],),
        sa.ForeignKeyConstraint(["track_id"], ["track.id"],),
        sa.PrimaryKeyConstraint("track_id", "playlist_id"),
    )


def downgrade() -> None:
    op.drop_table("playlist_tracks")
    op.drop_table("track")
    op.drop_table("artist")
