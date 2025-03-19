"""unique True to email

Revision ID: 7bea66aea817
Revises: 456a88aeb003
Create Date: 2025-03-19 12:47:51.376369

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7bea66aea817"
down_revision: Union[str, None] = "456a88aeb003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
