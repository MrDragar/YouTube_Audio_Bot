from aiogram import Dispatcher
import aioschedule

import asyncio
import os
import datetime


async def delete_old_files():
    directory = "video/"
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        a = os.path.getmtime(file_path)
        time = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(a)).seconds
        if time > 1800:
            os.remove(file_path)


async def register_services(dp: Dispatcher):
    aioschedule.every(30).minutes.do(delete_old_files)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)


if __name__ == "__main__":
    delete_old_files()
