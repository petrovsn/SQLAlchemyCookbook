from core_entities import *
from sqlalchemy.orm import selectinload, joinedload

engine = redeclare_db()


with Session(engine) as session:
    user1 = User(name = "Alice", posts = [Post(text="Alicetext1"),Post(text="Alicetext2")])
    user2 = User(name = "Bob", posts = [Post(text="Alicetext2")])
    session.add_all([user1, user2])
    session.commit()


print("Lazyload")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).where(User.name == "Jhonatan")
        result = session.execute(query)
        saved_user = result.scalar_one_or_none()

    print(saved_user)
    print(saved_user.addresses)
except Exception as e:
    print("Exception:",e)


print("SelectingLoad")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).options(selectinload(User.posts)).where(User.name == "Jhonatan")
        result = session.execute(query)
        saved_user = result.scalar_one_or_none()

    print(saved_user)
    print(saved_user.posts)
except Exception as e:
    print("Exception:",e)

print("JoinedLoad")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).options(joinedload(User.posts)).where(User.name == "Jhonatan")
        result = session.execute(query)
        saved_user = result.scalar_one_or_none()

    print(saved_user)
    print(saved_user.posts)
except Exception as e:
    print("Exception:",e)


print("SCALARS UNIQUE REQ")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).join(Post)
        result = session.execute(query)
        users = result.scalars()
        for user in users:
            print(user)

except Exception as e:
    print("Exception:",e)

print("SCALARS UNIQUE REQ")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).options(joinedload(User.posts))
        result = session.execute(query)
        users = result.scalars()
        for user in users:
            print(user)

except Exception as e:
    print("Exception:",e)

"""
Raiseload - блокирует lazyload
contains_eager(Address.user) - редкая стратегия, сначала пишем JOIN, 
а потом из него извлекаем данные для заполнения orm
"""