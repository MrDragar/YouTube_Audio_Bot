from datetime import date

from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.methods import SendMessage
from aiogram.handlers import MessageHandler

from bot.database.day_statistic import get_monthly_statistics, get_day_statistic
from bot.filters import IsAdmin

statistic_router = Router()


@statistic_router.message(Command("get_month_statistic"), IsAdmin())
class SentMonthlyStatisticHandler(MessageHandler):
    async def handle(self):
        result = await get_monthly_statistics(date.today())
        await SendMessage(chat_id=self.chat.id,
                          text="За этот месяц новых пользователей: {0} \n"
                               "Успешных запросов: {1} \n"
                               "Запросов с неотловленной ошибкой: {2}"
                          .format(result["new_users"],
                                  result["successful_requests"],
                                  result["unsuccessful_requests"]))


@statistic_router.message(Command("get_day_statistic"), IsAdmin())
class SentMonthlyStatisticHandler(MessageHandler):
    async def handle(self):
        result = await get_day_statistic()
        await SendMessage(chat_id=self.chat.id,
                          text="За этот день новых пользователей: {0} \n"
                               "Успешных запросов: {1} \n"
                               "Запросов с неотловленной ошибкой: {2}"
                          .format(result.new_users, result.successful_requests,
                                  result.unsuccessful_requests))
