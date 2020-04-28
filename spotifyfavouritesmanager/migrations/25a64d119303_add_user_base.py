"""Add user base

Revision ID: 25a64d119303
Revises:
Create Date: 2020-04-28 19:55:20.112943

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "25a64d119303"
down_revision = None
branch_labels = ("default",)
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("user")
