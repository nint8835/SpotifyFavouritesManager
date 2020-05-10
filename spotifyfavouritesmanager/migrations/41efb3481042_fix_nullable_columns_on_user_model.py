"""Fix nullable columns on user model

Revision ID: 41efb3481042
Revises: 2528a69ac8e8
Create Date: 2020-05-10 00:41:45.036904

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "41efb3481042"
down_revision = "2528a69ac8e8"
branch_labels = ()
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "user",
        "token_data",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    op.alter_column("user", "username", existing_type=sa.TEXT(), nullable=False)


def downgrade() -> None:
    op.alter_column("user", "username", existing_type=sa.TEXT(), nullable=True)
    op.alter_column(
        "user",
        "token_data",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
