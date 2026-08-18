from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer

engine = redeclare_db()

users = [
    {"name": f"name_{i}"}  for i in range(1000)
]

with Session(engine) as session:
    for user_dto in users:
        user = User(**user_dto)
        for i in range(10):
            user.posts.append(Post(text = f"post #{i} from {user.name}"))
        session.add(user)
    session.commit()

@performance_timer
def load_data_from_statement(stmt):
    posts_count = 0
    with Session(engine) as session:
        result: list[User] = session.execute(stmt).unique().scalars()
        for user in result:
            posts_count+=len(user.posts)
    print("Post count:", posts_count)
        
print("Lazyload")
lazy_load_stmt = select(User)
load_data_from_statement(lazy_load_stmt)


print("SelectingLoad")
selecting_load_stmt = select(User).options(selectinload(User.posts))
load_data_from_statement(selecting_load_stmt)

print("JoinedLoad")
selecting_load_stmt = select(User).options(joinedload(User.posts))
load_data_from_statement(selecting_load_stmt)


print("SubqueryLoad")
selecting_load_stmt = select(User).options(subqueryload(User.posts))
load_data_from_statement(selecting_load_stmt)

"""
Как применять:
joinedload    → одиночная relationship
selectinload  → коллекция
subqueryload  → специализированный/legacy-вариант
"""