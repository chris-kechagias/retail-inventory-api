"""initial_retail_schema

Revision ID: 0a15537c0ab3
Revises:
Create Date: 2026-04-08 22:50:27.643582

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0a15537c0ab3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Product Table
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "TEES",
                "SWEATERS",
                "SHIRTS",
                "PANTS",
                "SHORTS",
                "TANK_TOPS",
                "OTHER",
                name="category",
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("color", sa.String(length=30), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("collection", sa.String(length=10), nullable=True),
        sa.Column("coming_soon", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_name"), "product", ["name"], unique=False)

    # Create ProductVariant Table
    op.create_table(
        "productvariant",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("size", sa.Enum("S_M", "L_XL", "OS", name="size"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("in_stock", sa.Boolean(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("productvariant")
    op.drop_table("product")
