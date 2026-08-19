from core_entities import *

engine = redeclare_db()

data2load = [
    {"name":"Will"},
    {"name":"Bob"},
    {"name":None},
    {"name":"Edgar"},
]

    
with Session(engine) as session:
    for dto in data2load:
        """
        begin nected делает точку сохранения, ролбек идет до нее.
        """
        with session.begin_nested(): 
            try: 
                user = User(**dto)
                session.add(user)
                session.flush()
            except Exception as e:
                print(e)
                session.rollback()
    session.commit()


with Session(engine) as session:
    query = select(User)
    result = session.execute(query)
    for user in result.scalars():
        print(user)


with Session(engine) as session:
    user1 = User(name = "Alice")
    session.add(user1)
    session.flush()
    user2 = User(name = "AliceMad")
    session.add(user2)
    session.flush()
    #session.rollback()

    print("user1:", user1)

    user3 = User(name = "AliceMaddness ")
    session.add(user2)
    #session.commit()

    result = session.execute(query)
    for user in result.scalars():
        print(user)

with Session(engine) as session:
    query = select(User)
    result = session.execute(query)
    for user in result.scalars():
        print(user)