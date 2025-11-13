from asyncio.log
import logger # type: ignore
import datetime
from sqlite3 import Cursor
import types

from aiogram import Router
from matplotlib.pylab import conj


def init_db():
    try:
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS "reservations" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "user_id" INTEGER,
            "group_name" TEXT NOT NULL,
            "date" DATE NOT NULL,
            "status" TEXT DEFAULT 'active',
            "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        ''')

        conj.commit()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации базы данных: {e}")

def add_reservation(user_id, group_name, date):
    try:
        Cursor.execute('''
        INSERT INTO reservations (user_id, group_name, date)
        VALUES (?, ?, ?)
        ''', (user_id, group_name, date))
        conj.commit()
        logger.info(f"Бронь добавлена для пользователя {user_id} на группу {group_name} на дату {date}.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении брони: {e}")

def check_reservation(user_id, group_name, date):
    try:
        Cursor.execute('''
        SELECT * FROM reservations 
        WHERE user_id = ? AND group_name = ? AND date = ? AND status = 'active'
        ''', (user_id, group_name, date))
        return Cursor.fetchall()
    except Exception as e:
        logger.error(f"Ошибка при проверке броней: {e}")
        return None

@Router.message(commands=['add_reservation'])
async def handle_add_reservation(message: types.Message):
    user_id = message.from_user.id
    group_name = "Группа 1"
    date = datetime.date.today().isoformat()

    add_reservation(user_id, group_name, date)
    await message.answer("✅ Бронь успешно добавлена!")

@Router.message(commands=['check_reservation'])
async def handle_check_reservation(message: types.Message):
    user_id = message.from_user.id
    group_name = "Группа 1"
    date = datetime.date.today().isoformat()

    reservations = check_reservation(user_id, group_name, date)
    if reservations:
        await message.answer("📅 У вас есть активные брони на сегодня.")
    else:
        await message.answer("❌ У вас нет активных броней на сегодня.")