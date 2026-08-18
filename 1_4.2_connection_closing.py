from core_entities import *
from sqlalchemy import text

engine = create_engine("sqlite+pysqlite:///connection_leak.db", 

                        pool_size=1000,
                        max_overflow=10,
                        pool_timeout=2,
                       echo=True, future=True)
Base.metadata.create_all(engine)
session = Session(engine)

user = User(name = "Alice")

session.add(user)
session.commit()

#CLOSE ТОЛЬКО ОСВОБОЖДАЕТ РЕСУРСЫ, НО НЕ УНИЧТОЖАЕТ ОБЪЕКТ
session.close()


session.add(User(name = "Dilan"))
session.commit()