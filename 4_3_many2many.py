from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer
from sqlalchemy import Table

user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("users_v2.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class User_v2(Base):
    __tablename__ = "users_v2"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    groups: Mapped[list["Group"]] = relationship(
        secondary=user_group,
        back_populates="users",
    )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["User_v2"]] = relationship(
        secondary=user_group,
        back_populates="groups",
    )

engine = redeclare_db()

with Session(engine) as session:
    user = User_v2(name="Alice")

    user.groups = [
        Group(name="Administrators"),
        Group(name="Administrators2"),
        Group(name="Administrators3")
    ]

    session.add(user)
    session.commit()



with Session(engine) as session:
    result = session.execute(select(Group))
    for row in result.scalars():
        print(row)


    result = session.execute(select(User_v2))
    for row in result.scalars():
        print(row)




    #result = session.execute(delete(Group))
    #session.flush()

    result = session.execute(select(Group))
    for row in result.scalars():
        session.delete(row)

    result = session.execute(select(User_v2))
    for row in result.scalars():
        print(row, row.groups)


    result = session.execute(select(user_group))
    for row in result.mappings():
        print(row)