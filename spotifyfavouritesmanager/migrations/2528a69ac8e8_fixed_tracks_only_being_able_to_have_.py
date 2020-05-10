"""Fixed tracks only being able to have one artist

Revision ID: 2528a69ac8e8
Revises: 8bd75fcafb3f
Create Date: 2020-05-09 23:54:46.757844

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2528a69ac8e8"
down_revision = "8bd75fcafb3f"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.create_table(
        "track_artists",
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("artist_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["artist_id"], ["artist.id"],),
        sa.ForeignKeyConstraint(["track_id"], ["track.id"],),
        sa.PrimaryKeyConstraint("track_id", "artist_id"),
    )
    op.drop_constraint("track_artist_id_fkey", "track", type_="foreignkey")
    op.drop_column("track", "artist_id")


def downgrade() -> None:
    op.add_column(
        "track",
        sa.Column("artist_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "track_artist_id_fkey", "track", "artist", ["artist_id"], ["id"]
    )
    op.drop_table("track_artists")
