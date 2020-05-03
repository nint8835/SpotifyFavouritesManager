"""Add token details column to user

Revision ID: 9536f5b2b213
Revises: 25a64d119303
Create Date: 2020-05-03 18:27:05.322276

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9536f5b2b213"
down_revision = "25a64d119303"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("token_data", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "token_data")
