from core_entities import *
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from core_utils import performance_timer

engine = redeclare_db()
#session.query(User).filter(User.active == True).update({"status": "inactive"})

with Session(engine) as session:
    user1 = User(name = "Alice",
                posts = [
                    Post(text = "Hello, kitty"),
                    Post(text = "Praise the sun" )
                ])

    user2 = User(name = "Bob",
                    posts = [
                        Post(text = "#ironwithin"),
                        Post(text = "#ironwithout" )
                    ])

    user3 = User(name = "Charlie")

    session.add_all([user1, user2,user3])


    session.commit()


with Session(engine) as session:
    result =  session.execute(select(User.name, Post.text).join(Post, User.id == Post.user_id))
    for row in result.mappings():
        print(row)


with Session(engine) as session:
    user = session.get(User, 1)
    user.posts = []
    session.flush()
    session.delete(user)

    result =  session.execute(select(User.name, Post.text).join(Post, User.id == Post.user_id))
    for row in result.mappings():
        print(row)


    result =  session.execute(select(Post))
    for row in result.scalars():
        print(row)