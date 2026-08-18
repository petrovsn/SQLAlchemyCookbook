from core_entities import *
from sqlalchemy import text

sessions = []  # храним сессии, чтобы они не удалялись GC
engine = create_engine("sqlite+pysqlite:///connection_leak.db", 

                        pool_size=1000,
                        max_overflow=10,
                        pool_timeout=2,
                       echo=True, future=True)


try:
    for i in range(1, 10001):
        print(f"\n--- Итерация {i} ---")
        sess = Session(engine)
        # Делаем какую-нибудь операцию, чтобы соединение реально захватилось
        sess.execute(text("SELECT 1"))  # или любая другая команда
        sessions.append(sess)
        print(f"Активных сессий: {len(sessions)}")
        sess.close()

        sess.close()
        
except Exception as e:
    print(f"\n❌ Ошибка на итерации {i}: {e}")
    print(f"Успешно создано сессий: {i-1}")

for sess in sessions:
    sess.close()