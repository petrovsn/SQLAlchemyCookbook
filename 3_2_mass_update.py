from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer

engine = redeclare_db()

users = [
    {"name": f"name_{i}"}  for i in range(1000)
]

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

