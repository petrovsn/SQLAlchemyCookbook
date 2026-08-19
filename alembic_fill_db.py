from alembic_src.engine import redeclare_db
from alembic_src.models import User, Post
from sqlalchemy.orm import Session
from sqlalchemy import insert
import random

engine = redeclare_db()

with Session(engine) as session:
    names = ["Alice", "Bob", "Charly"]
    posts = ["Hello, world!", "I love you!", "I hate everything about you", "Cats are best", "Peace!"]
    session.execute(insert(User),[{"name":name} for name in names])
    for post in posts:
        random_user_id = random.randint(1,3)
        user = session.get(User, random_user_id)
        user.posts.append(Post(text = post))
        session.flush()
    session.commit()