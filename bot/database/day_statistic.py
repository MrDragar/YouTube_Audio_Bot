from datetime import date

from .models import DayStatistic


async def get_day_statistic() -> DayStatistic:
    day_statistic = await DayStatistic.get_or_create(date=date.today())
    return day_statistic[0]


async def add_user():
    day_statistic = await get_day_statistic()
    day_statistic.new_users += 1
    await day_statistic.save()


async def add_successful_request():
    day_statistic = await get_day_statistic()
    day_statistic.successful_requests += 1
    await day_statistic.save()


async def add_unsuccessful_request():
    day_statistic = await get_day_statistic()
    day_statistic.unsuccessful_requests += 1
    await day_statistic.save()
