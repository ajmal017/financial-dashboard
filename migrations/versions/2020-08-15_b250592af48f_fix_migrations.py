"""fix migrations

Revision ID: b250592af48f
Revises: a3f836d85d38
Create Date: 2020-08-15 05:44:11.663114

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b250592af48f"
down_revision = "a3f836d85d38"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stock_history")
    op.alter_column(
        "portfolio",
        "name",
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
        existing_server_default=sa.text("'Default'::character varying"),
    )
    op.create_unique_constraint("uq_portfolio_name", "portfolio", ["name"])
    op.drop_constraint(
        "portfolio_stocks_portfolio_id_fkey", "portfolio_stocks", type_="foreignkey"
    )
    op.drop_constraint(
        "portfolio_stocks_stock_id_fkey", "portfolio_stocks", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_portfolio_stocks_portfolio_id_portfolio"),
        "portfolio_stocks",
        "portfolio",
        ["portfolio_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_portfolio_stocks_stock_id_stocks"),
        "portfolio_stocks",
        "stocks",
        ["stock_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("portfolio_stocks", "id")
    op.create_unique_constraint(op.f("uq_roles_name"), "roles", ["name"])
    op.drop_constraint("roles_name_key", "roles", type_="unique")
    op.create_unique_constraint("uq_stocks_ticker", "stocks", ["ticker"])
    op.drop_constraint("stocks_ticker_key", "stocks", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("stocks_ticker_key", "stocks", ["ticker"])
    op.drop_constraint("uq_stocks_ticker", "stocks", type_="unique")
    op.create_unique_constraint("roles_name_key", "roles", ["name"])
    op.drop_constraint(op.f("uq_roles_name"), "roles", type_="unique")
    op.add_column(
        "portfolio_stocks",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_portfolio_stocks_stock_id_stocks"),
        "portfolio_stocks",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_portfolio_stocks_portfolio_id_portfolio"),
        "portfolio_stocks",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "portfolio_stocks_stock_id_fkey",
        "portfolio_stocks",
        "stocks",
        ["stock_id"],
        ["id"],
    )
    op.create_foreign_key(
        "portfolio_stocks_portfolio_id_fkey",
        "portfolio_stocks",
        "portfolio",
        ["portfolio_id"],
        ["id"],
    )
    op.create_unique_constraint("portfolio_name_key", "portfolio", ["name"])
    op.drop_constraint("uq_portfolio_name", "portfolio", type_="unique")
    op.alter_column(
        "portfolio",
        "name",
        existing_type=sa.VARCHAR(length=50),
        nullable=True,
        existing_server_default=sa.text("'Default'::character varying"),
    )
    op.create_table(
        "stock_history",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("stock_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("close", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("open", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("high", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("low", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("dividends", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("volume", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["stock_id"],
            ["stocks.id"],
            name="stock_history_stock_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="stock_history_pkey"),
    )
    # ### end Alembic commands ###
