from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer

engine = redeclare_db()

users = [
    {"name": f"name_{i}"}  for i in range(1000)
]



from sqlalchemy import select, func
def count_rows(model_cls):
    with Session(engine) as session:
        total_posts = session.scalar(
            select(func.count()).select_from(model_cls)
        )
        print(f"rows count in {model_cls.__name__}:", total_posts)


@performance_timer
def upload_add_all():
    with Session(engine) as session:
        users_objects = []
        for user_dto in users:
            user = User(**user_dto)
            for i in range(10):
                user.posts.append(Post(text = f"post #{i} from {user.name}"))
            users_objects.append(user)
        session.add_all(users_objects)
        session.commit()

@performance_timer
def bulk_insert_mappings():
    with Session(engine) as session:
        session.bulk_insert_mappings(
            User,
            [
                {"name": f"name_{i}",
                "posts": [Post(text = f"post #{i} from name_{i}") for i in range(10)]}
                for i in range(1000)
            ]
        )

        session.commit()

@performance_timer
def insert_data():
    with Session(engine) as session:
        result = session.execute(
            insert(User).returning(User.id),
            [
                {"name": f"name_{i}"}
                for i in range(10000)
            ]
        )

        session.commit()
        return result.scalars().all()


ids = insert_data()

count_rows(User)

count_rows(Post)

with Session(engine) as session:
    user = session.get(User, 1)
    print(user)
    print(user.posts)