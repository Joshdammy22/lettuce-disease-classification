"""First migration.

Revision ID: b42dbf9cf21a
Revises: 
Create Date: 2024-07-24 21:13:20.068782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42dbf9cf21a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('disease_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('causes', sa.Text(), nullable=False),
    sa.Column('recommendation_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.Column('email_verification_token', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(length=255), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnoses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('disease_info_id', sa.Integer(), nullable=True),
    sa.Column('diagnosis', sa.String(length=100), nullable=False),
    sa.Column('confidence_score', sa.Float(), nullable=False),
    sa.Column('diagnosis_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['disease_info_id'], ['disease_info.id'], ),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diagnosis_id', sa.Integer(), nullable=False),
    sa.Column('accuracy_feedback', sa.String(length=200), nullable=True),
    sa.Column('recommendation_feedback', sa.String(length=200), nullable=True),
    sa.Column('feedback_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['diagnosis_id'], ['diagnoses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    op.drop_table('diagnoses')
    op.drop_table('images')
    op.drop_table('users')
    op.drop_table('disease_info')
    # ### end Alembic commands ###