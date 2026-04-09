"""migrate_to_uuid_pks_and_add_sku

Revision ID: b2f4e891c3d7
Revises: 0a15537c0ab3
Create Date: 2026-04-09 10:00:00.000000

Migrates product and productvariant tables from integer PKs to UUID PKs.
Adds auto-generated SKU field to product (format: TS-0001, SW-0003, etc.).

Downgrade is intentionally destructive — not intended for production rollback.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b2f4e891c3d7"
down_revision: Union[str, Sequence[str], None] = "0a15537c0ab3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Step 1: Add new UUID columns (server_default populates existing rows) ──
    op.add_column(
        "product",
        sa.Column(
            "new_id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
    )
    op.add_column(
        "product",
        sa.Column("sku", sa.String(length=7), nullable=True),
    )
    op.add_column(
        "productvariant",
        sa.Column(
            "new_id",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
    )
    op.add_column(
        "productvariant",
        sa.Column("new_product_id", postgresql.UUID(), nullable=True),
    )

    # ── Step 2: Populate SKUs for existing rows ────────────────────────────────
    # Uses ROW_NUMBER() partitioned by category to assign sequential SKUs.
    # Handles both possible enum value formats (e.g. 'Tees' and 'TEES').
    op.execute("""
        UPDATE product p
        SET sku = sub.sku
        FROM (
            SELECT id,
                   CONCAT(
                       CASE category::text
                           WHEN 'Tees'      THEN 'TS'
                           WHEN 'TEES'      THEN 'TS'
                           WHEN 'Sweaters'  THEN 'SW'
                           WHEN 'SWEATERS'  THEN 'SW'
                           WHEN 'Shirts'    THEN 'ST'
                           WHEN 'SHIRTS'    THEN 'ST'
                           WHEN 'Pants'     THEN 'PT'
                           WHEN 'PANTS'     THEN 'PT'
                           WHEN 'Shorts'    THEN 'SH'
                           WHEN 'SHORTS'    THEN 'SH'
                           WHEN 'Tank Tops' THEN 'TT'
                           WHEN 'TANK_TOPS' THEN 'TT'
                           ELSE 'OR'
                       END,
                       '-',
                       LPAD(
                           ROW_NUMBER() OVER (PARTITION BY category ORDER BY id)::text,
                           4, '0'
                       )
                   ) AS sku
            FROM product
        ) sub
        WHERE p.id = sub.id
    """)

    # ── Step 3: Link new_product_id in variants to product.new_id ─────────────
    op.execute("""
        UPDATE productvariant v
        SET new_product_id = p.new_id
        FROM product p
        WHERE v.product_id = p.id
    """)

    # ── Step 4: Drop FK constraint on productvariant ───────────────────────────
    op.drop_constraint(
        "productvariant_product_id_fkey", "productvariant", type_="foreignkey"
    )

    # ── Step 5: Drop old integer PK columns ───────────────────────────────────
    op.drop_column("productvariant", "id")
    op.drop_column("productvariant", "product_id")
    op.drop_column("product", "id")

    # ── Step 6: Rename new UUID columns into place ─────────────────────────────
    op.alter_column("product", "new_id", new_column_name="id")
    op.alter_column("productvariant", "new_id", new_column_name="id")
    op.alter_column(
        "productvariant", "new_product_id", new_column_name="product_id", nullable=False
    )
    # SKU must be non-null and unique after backfill
    op.alter_column("product", "sku", nullable=False)

    # ── Step 7: Recreate PK and FK constraints ─────────────────────────────────
    op.create_primary_key("pk_product", "product", ["id"])
    op.create_primary_key("pk_productvariant", "productvariant", ["id"])
    op.create_foreign_key(
        "productvariant_product_id_fkey",
        "productvariant",
        "product",
        ["product_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # ── Step 8: Unique constraint on SKU ──────────────────────────────────────
    op.create_unique_constraint("uq_product_sku", "product", ["sku"])


def downgrade() -> None:
    # Note: reversing UUID → int is destructive and not supported automatically.
    # To rollback, restore from a DB snapshot taken before this migration.
    raise NotImplementedError(
        "Downgrade from UUID PKs to integer PKs is not supported. "
        "Restore from a database snapshot instead."
    )
