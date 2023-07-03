from .models import User


async def get_user_by_id(id: int) -> User:
    return await User.get_or_none(id=id)


async def create_user(id: int, name: str, language: str) -> User:
    user = await get_user_by_id(id)
    if not user:
        user = await User.create(id=id, name=name, language=language)
        await user.save()
    return user


async def get_users() -> list[User]:
    return await User.all()


async def change_language(id: int, language: str) -> None:
    user = await get_user_by_id(id)
    user.language = language
    await user.save()
