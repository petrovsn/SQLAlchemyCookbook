from core_entities_async import *
import asyncio


async def task_1(session):
    print("TASK 1: start")

    user = User(name="Alice")
    session.add(user)

    await session.flush()

    print("TASK 1: sleeping...")
    await asyncio.sleep(1)

    await session.commit()

    print("TASK 1: done")


async def task_2(session):
    print("TASK 2: start")

    user = User(name="Bob")
    session.add(user)

    await session.flush()

    print("TASK 2: sleeping...")


    await session.commit()

    print("TASK 2: done")


async def main():
    engine = await redeclare_db_async(echo=True)

    session = AsyncSession(engine)

    #НЕ НАДО ТАК ДЕЛАТЬ
    """
    Когда таск 1 делает флаш и передает управление, 
    таск 2 начинает делать свой флаш, пока первый еще не закончился
    и сессия еще к нему не готова, после чего падает с ошибкой
    InvalidRequestError Session is already flushing
    """
    try:
        await asyncio.gather(
            task_1(session),
            task_2(session),
        )
    except Exception as e:
        print(type(e).__name__, e)

    await session.close()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())