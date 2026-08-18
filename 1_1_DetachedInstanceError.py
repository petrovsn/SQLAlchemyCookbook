from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import select, update, delete
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

# Твой код с моделями и engine = create_engine(...) должен быть выше

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Проверяем, что мы работаем именно с SQLite
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

@as_declarative() 
class Base(object): 
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)

    def to_dict(self):
        """
        Преобразует объект модели в словарь.
        Возвращает все колонки таблицы.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def  __repr__(self):
        return str(self.to_dict())

class User(Base): 
    __tablename__ = "users"
    name = Column(String) 
    nickname = Column(String, nullable=True) 
    addresses = relationship("Address", back_populates="user") 
    posts = relationship("Post", back_populates="user") 
 
 
class Address(Base): 
    __tablename__ = "addresses"
    email_address = Column(String, nullable=False) 
    user_id = Column(Integer, ForeignKey("users.id")) 
    user = relationship("User", back_populates="addresses") 



class Post(Base): 
    __tablename__ = "posts"
    text = Column(String) 
    user_id = Column(Integer, ForeignKey("users.id")) 
    user = relationship("User", back_populates="posts") 


for model in [User,Address, Post]:
    print(model.__table__)

Base.metadata.create_all(engine)

with Session(engine) as session:
    user = User(name = "Jhonatan")
    session.add(user)
    user.addresses.append(Address(email_address = "JhonDow@mail"))
    user.addresses.append(Address(email_address = "JhonDow2@mail"))

    user = User(name = "Jennny")
    session.add(user)
    session.flush()
    session.commit()

saved_user = None
with Session(engine) as session:
    query = select(User).where(User.name == "Jhonatan")
    result = session.execute(query)
    saved_user = result.scalar_one_or_none()

print(saved_user)
print(saved_user.addresses)
    


