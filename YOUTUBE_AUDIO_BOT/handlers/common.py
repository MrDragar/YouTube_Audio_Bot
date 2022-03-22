from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def send_welcome(message: types.Message):
    await message.reply("""Привет. Я "Скачать звук с YouTube". Если хочешь получить звук видео из YouTube, тебе
     нужно написать мне url адрес видео. Чтобы сделать это, открой видео в мобильном приложении YouTube, нажми на
      кнопку "Поделиться", выберите Телеграмм отправьте мне сообщение.""")
