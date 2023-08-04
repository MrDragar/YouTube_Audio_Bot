from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import datetime


async def delete_old_files():
    directory = "video/"
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        a = max(os.path.getctime(file_path), os.path.getatime(file_path),
                os.path.getmtime(file_path))
        time = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(a)).seconds
        try:
            if time > 1200:
                os.remove(file_path)
        finally:
            ...


def register_services():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_old_files, trigger="interval", minutes=2)
    scheduler.start()
