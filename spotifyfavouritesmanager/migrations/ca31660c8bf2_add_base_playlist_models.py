"""Add base playlist models

Revision ID: ca31660c8bf2
Revises: 9536f5b2b213
Create Date: 2020-05-08 23:37:18.336702

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ca31660c8bf2"
down_revision = "9536f5b2b213"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.create_table(
        "playlist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("spotify_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("playlist_type", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "monthly_playlist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month", sa.Text(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id"], ["playlist.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "yearly_playlist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id"], ["playlist.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("yearly_playlist")
    op.drop_table("monthly_playlist")
    op.drop_table("playlist")
