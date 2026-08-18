from core_entities_async import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer, performance_timer_async
import asyncio

users = [
    {"name": f"name_{i}"}  for i in range(1000)
]

@performance_timer_async
async def load_data_from_statement(stmt, engine):
    posts_count = 0
    async with AsyncSession(engine) as session:
        result: list[User] = (await session.execute(stmt)).unique().scalars()
        for user in result:
            posts_count+= len(
                await user.awaitable_attrs.posts
            )
    print("Post count:", posts_count)


async def main():
    engine = await redeclare_db_async(echo = False)

    print("start async")
    async with AsyncSession(engine) as session:
        for user_dto in users:
            user = User(**user_dto)
            for i in range(10):
                user.posts.append(Post(text = f"post #{i} from {user.name}"))
            session.add(user)
        await session.commit()


    print("Lazyload")
    lazy_load_stmt = select(User)
    await load_data_from_statement(lazy_load_stmt, engine)

    print("SelectingLoad")
    selecting_load_stmt = select(User).options(selectinload(User.posts))
    await load_data_from_statement(selecting_load_stmt, engine)

    print("JoinedLoad")
    selecting_load_stmt = select(User).options(joinedload(User.posts))
    await load_data_from_statement(selecting_load_stmt, engine)


    print("SubqueryLoad")
    selecting_load_stmt = select(User).options(subqueryload(User.posts))
    await load_data_from_statement(selecting_load_stmt, engine)


    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())