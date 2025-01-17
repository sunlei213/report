"""initial migration

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建manager_groups表
    op.create_table('manager_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建managers表
    op.create_table('managers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['manager_groups.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建product_groups表
    op.create_table('product_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建products表
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('min_amount', sa.Numeric(precision=18, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['product_groups.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # 创建client_relations表
    op.create_table('client_relations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account', sa.String(length=50), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('fenchen', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('serial_no', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('account'),
        sa.UniqueConstraint('serial_no')
    )

    # 创建transactions表
    op.create_table('transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('account', sa.String(length=50), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('product_code', sa.String(length=50), nullable=False),
        sa.Column('product_name', sa.String(length=100), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column('serial_no', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('serial_no')
    )

    # 创建adjustments表
    op.create_table('adjustments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('account', sa.String(length=50), nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('product_code', sa.String(length=50), nullable=False),
        sa.Column('product_name', sa.String(length=100), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column('reason', sa.String(length=200), nullable=True),
        sa.Column('remark', sa.String(length=500), nullable=True),
        sa.Column('serial_no', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('serial_no')
    )

    # 创建索引
    op.create_index('idx_date_account', 'transactions', ['date', 'account'])
    op.create_index('idx_product_code', 'transactions', ['product_code'])
    op.create_index('idx_serial_no', 'transactions', ['serial_no'])
    
    op.create_index('idx_adjustment_date', 'adjustments', ['date'])
    op.create_index('idx_adjustment_account', 'adjustments', ['account'])
    op.create_index('idx_adjustment_product', 'adjustments', ['product_code'])
    op.create_index('idx_adjustment_serial', 'adjustments', ['serial_no'])
    
    op.create_index('idx_account', 'client_relations', ['account'])
    op.create_index('idx_client_relation_serial', 'client_relations', ['serial_no'])

def downgrade():
    # 删除所有表
    op.drop_table('adjustments')
    op.drop_table('transactions')
    op.drop_table('client_relations')
    op.drop_table('products')
    op.drop_table('product_groups')
    op.drop_table('managers')
    op.drop_table('manager_groups') 