from core_entities import *


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