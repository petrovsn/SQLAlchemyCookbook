"""
python
session.query(User).filter(User.active == True).update({"status": "inactive"})
Исследовать:

Что произойдёт с объектами уже загруженными в сессию?

Параметр synchronize_session='fetch' vs 'evaluate' — в чём разни
"""


from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer

engine = redeclare_db("mass_update.db", echo = False)
#session.query(User).filter(User.active == True).update({"status": "inactive"})

with Session(engine) as session:
    session.execute(delete(User))
    session.commit()

users = [
    {"name": f"name_{i}"}  for i in range(10)
]

@performance_timer
def insert_data():
    with Session(engine) as session:
        result = session.execute(
            insert(User).returning(User.id),
            users
        )
        session.commit()
        return result.scalars().all()
insert_data()


print("ContextONE")
with Session(engine) as session:
    result = session.execute(select(User))
    users = result.scalars().all()
    print("BEFORE ALTERATION")
    for user in users:
            print(user)

    stmt = update(User).where(User.nickname == None
                              ).values(nickname = "NickLeft"
                                       ).execution_options(
        synchronize_session="fetch"
    )
    session.execute(stmt)
    #session.commit()

    #result = session.execute(select(User))
    #users = result.scalars().all()

    print("AFTER ALTERATION")
    for user in users:
        print(user)