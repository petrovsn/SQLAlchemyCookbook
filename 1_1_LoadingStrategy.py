from core_entities import *
from sqlalchemy.orm import selectinload, joinedload

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
        query = select(User).options(selectinload(User.addresses)).where(User.name == "Jhonatan")
        result = session.execute(query)
        saved_user = result.scalar_one_or_none()

    print(saved_user)
    print(saved_user.addresses)
except Exception as e:
    print("Exception:",e)

print("JoinedLoad")
try:
    saved_user = None
    with Session(engine) as session:
        query = select(User).options(joinedload(User.addresses)).where(User.name == "Jhonatan")
        result = session.execute(query)
        saved_user = result.scalar_one_or_none()

    print(saved_user)
    print(saved_user.addresses)
except Exception as e:
    print("Exception:",e)



"""
Raiseload - блокирует lazyload
contains_eager(Address.user) - редкая стратегия, сначала пишем JOIN, 
а потом из него извлекаем данные для заполнения orm
"""