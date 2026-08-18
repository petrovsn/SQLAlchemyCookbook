from core_entities import *

requested_id = None
with Session(engine) as session:
    user = User(name = "Alice")
    session.add(user)
    session.commit()
    requested_id = user.id


with Session(engine) as session:
    user_loaded = session.get(User, requested_id)
    print(user_loaded)
    print(user)
    print("Is equal:", user_loaded == user)
    print("Is the same:",user_loaded is user)

    user_loaded.name = "Alan"

    session.flush()

    print("After flush:", user_loaded.name)


    session.commit()
    
    print("After commit:", user_loaded.name)
