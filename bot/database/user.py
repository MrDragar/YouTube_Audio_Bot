from models import User


async def create_user(id, name: str, language: str) -> User:
    user = User(id=id, name=name, language=language)
    await user.save()
    return user


async def get_users() -> list[User]:
    return await User.all()


async def get_user_by_id(id: int) -> User:
    return await User.get_or_none(id=id)
