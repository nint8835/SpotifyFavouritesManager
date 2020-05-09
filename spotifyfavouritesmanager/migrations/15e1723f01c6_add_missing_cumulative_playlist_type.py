"""Add missing cumulative playlist type

Revision ID: 15e1723f01c6
Revises: ca31660c8bf2
Create Date: 2020-05-09 00:21:28.651743

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "15e1723f01c6"
down_revision = "ca31660c8bf2"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cumulative_playlist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id"], ["playlist.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("cumulative_playlist")
