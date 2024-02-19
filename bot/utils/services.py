import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from functools import wraps

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import datetime


def run_async(function: Callable):
    @wraps(function)
    async def wrapper():
        loop = asyncio.get_running_loop()
        """Запускает функцию в потоке"""
        with ThreadPoolExecutor() as pool:
            task = loop.run_in_executor(pool, function)
            await asyncio.gather(task)
    return wrapper


@run_async
def delete_old_files():
    directory = "video/"
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        a = max(os.path.getctime(file_path), os.path.getatime(file_path),
                os.path.getmtime(file_path))
        time = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(a)).seconds
        try:
            if time > 360:
                os.remove(file_path)
        finally:
            ...


def register_services():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_old_files, trigger="interval", minutes=3)
    scheduler.start()
