from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer
import random
from sqlalchemy import select, func
from sqlalchemy import Table, Column, String, MetaData
import time

def count_rows(model_cls):
    with Session(engine) as session:
        total_posts = session.scalar(
            select(func.count()).select_from(model_cls)
        )
        print(f"rows count in {model_cls.__name__}:", total_posts)

@performance_timer
def insert_data(model_cls, data):
    with Session(engine) as session:
        result = session.execute(
            insert(model_cls).returning(model_cls.id),
            data
        )
        session.commit()
        return result.scalars().all()

N_USERS = 100000
N_POSTS_PER_USER = 10

engine = redeclare_db()

users_raw = [
    {"name": f"name_{i}"}  for i in range(N_USERS)
]
posts_raw = [{
    "user_name":user["name"],
    "text":f"post #{i} from {user["name"]}"} 
    for i in range(N_POSTS_PER_USER) for user in users_raw]

random.shuffle(users_raw)
random.shuffle(posts_raw)

print("Input users count:", len(users_raw))
print("Input posts count:", len(posts_raw))

users_ids = insert_data(User, users_raw)

print("Uploaded user:", len(users_ids))


metadata = MetaData()
staging_posts = Table(
    "staging_posts",
    metadata,
    Column("user_name", String),
    Column("text", String),
)
metadata.create_all(engine)

with Session(engine) as session:
    result = session.execute(
            insert(staging_posts),
            posts_raw
        )
    session.commit()

start_time = time.perf_counter()
with Session(engine) as session:
    stmt = (insert(Post)
            .from_select(
                ["user_id", "text"],
                select(
                    User.id,
                    staging_posts.c.text,
                )
                .join(
                    staging_posts,
                    User.name == staging_posts.c.user_name,
                )
            )
        )


    result = session.execute(stmt)
    session.commit()

stop_time = time.perf_counter()
print("Insertion time:", stop_time-start_time)


with engine.begin() as conn:
    staging_posts.drop(conn)
 
with Session(engine) as session:
    user = session.get(User, 10)
    print(user.name, user.posts)
