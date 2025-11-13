import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import io
import sqlite3
import datetime
from sqlite3 import Cursor
import types
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import re
import matplotlib.pyplot as plt
from aiogram import types
from aiogram.fsm.context import FSMContext
from db.database import cursor, conn # type: ignore
from fsm.states import Registration # type: ignore
from ui.keyboards import get_main_keyboard # type: ignore
from handlers import router # type: ignore # type: ignore
import csv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Конфигурация
BOT_TOKEN = "8137628454:AAEUPW8fKH3Jg7Edl47gME46MHEENk6RFZQ"
ADMIN_ID = 5559465220  # Ваш ID в Telegram

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище данных (временное, лучше использовать БД
def parse_file(file_content: bytes, file_type: str) -> list:
    """Парсинг CSV/Excel файла и возвращение списка студентов"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_type == 'excel':
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            return None
        
        # Преобразование в список словарей
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return None

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Отправьте CSV/Excel файл со студентами для импорта")

@dp.message(lambda message: message.document)
async def handle_file(message: types.Message):
    # Проверка прав доступа
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступ запрещен")
        return

    file = message.document
    file_type = file.file_name.split('.')[-1].lower()

    if file_type not in ['csv', 'xlsx']:
        await message.answer("Поддерживаются только CSV и Excel файлы")
        return

    try:
        # Скачивание файла
        file_content = await bot.download(file)
        parsed_data = parse_file(file_content.read(), file_type)

        if not parsed_data:
            await message.answer("Ошибка чтения файла")
            return

        # Обработка данных
        required_columns = ['name', 'group', 'student_id']
        for row in parsed_data:
            if all(col in row for col in required_columns):
                students.append({ # type: ignore
                    'name': row['name'],
                    'group': row['group'],
                    'student_id': row['student_id']
                })

        await message.answer(f"Успешно импортировано {len(students)} студентов") # type: ignore
        
        # Вывод первых 5 записей для проверки
        preview = "\n".join([f"{s['name']} - {s['group']}" for s in students[:5]]) # type: ignore
        await message.answer(f"Первые записи:\n{preview}")

    except Exception as e:
        await message.answer(f"Ошибка обработки файла: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())