"""tg_link is mandatory

Revision ID: 33aa93d68ad7
Revises: 042bbc4b6f7d
Create Date: 2026-08-19 13:50:22.657710
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "33aa93d68ad7"
down_revision: Union[str, Sequence[str], None] = "042bbc4b6f7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # 1. Заполняем tg_link у существующих пользователей
    # ---------------------------------------------------------

    users = sa.table(
        "users",
        sa.column("name", sa.String),
        sa.column("tg_link", sa.String),
    )

    op.execute(
        sa.update(users).values(
            tg_link="@" + users.c.name
        )
    )

    # ---------------------------------------------------------
    # 2. Создаём временную таблицу posts БЕЗ foreign key
    # ---------------------------------------------------------

    op.execute(
        sa.text("""
            CREATE TABLE posts_tmp (
                id INTEGER NOT NULL,
                text VARCHAR,
                user_id INTEGER,
                PRIMARY KEY (id)
            )
        """)
    )

    # ---------------------------------------------------------
    # 3. Копируем posts → posts_tmp
    # ---------------------------------------------------------

    op.execute(
        sa.text("""
            INSERT INTO posts_tmp (id, text, user_id)
            SELECT id, text, user_id
            FROM posts
        """)
    )

    # ---------------------------------------------------------
    # 4. Удаляем оригинальный posts
    #
    # Теперь FK posts → users больше не существует.
    # Поэтому users можно пересоздать.
    # ---------------------------------------------------------

    op.drop_table("posts")

    # ---------------------------------------------------------
    # 5. Пересоздаём users через batch_alter_table
    # ---------------------------------------------------------

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "tg_link",
            existing_type=sa.VARCHAR(),
            nullable=False,
        )

    # ---------------------------------------------------------
    # 6. Создаём posts обратно
    #
    # Теперь FK снова указывает на существующую users.
    # ---------------------------------------------------------

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    # ---------------------------------------------------------
    # 7. Возвращаем данные
    # ---------------------------------------------------------

    op.execute(
        sa.text("""
            INSERT INTO posts (id, text, user_id)
            SELECT id, text, user_id
            FROM posts_tmp
        """)
    )

    # ---------------------------------------------------------
    # 8. Временная таблица больше не нужна
    # ---------------------------------------------------------

    op.drop_table("posts_tmp")


def downgrade() -> None:

    # ---------------------------------------------------------
    # В downgrade нам снова нужно сделать tg_link nullable.
    # Это уже не требует удаления posts вручную,
    # поэтому batch может пересоздать users.
    # ---------------------------------------------------------

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "tg_link",
            existing_type=sa.VARCHAR(),
            nullable=True,
        )