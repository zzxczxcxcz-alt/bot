import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Конфигурация
BOT_TOKEN = "8137628454:AAEUPW8fKH3Jg7Edl47gME46MHEENk6RFZQ"  # Замените на ваш токен
ADMIN_ID = 5559465220  # Ваш ID в Telegram

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Пример данных
topics = {
    "my_topic": "Тема по программированию",
    "free_topics": ["Тема по искусственному интеллекту", "Тема по машинному обучению"],
    "students": {
        "student_x": {"name": "Студент X", "topic": None},
        "student_y": {"name": "Студент Y", "topic": "Тема по программированию"},
    }
}

# Создание клавиатуры
def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/my_topic"))
    keyboard.add(KeyboardButton("/free_topics"))
    keyboard.add(KeyboardButton("/contact_supervisor"))
    return keyboard

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Выберите команду:", reply_markup=create_keyboard())

@dp.message(Command("my_topic"))
async def my_topic_handler(message: types.Message):
    topic = topics["my_topic"]
    await message.answer(f"Ваша тема: {topic}", reply_markup=create_keyboard())

@dp.message(Command("free_topics"))
async def free_topics_handler(message: types.Message):
    free_topics = "n".join(topics["free_topics"])
    await message.answer(f"Свободные темы:n{free_topics}", reply_markup=create_keyboard())

@dp.message(Command("contact_supervisor"))
async def contact_supervisor_handler(message: types.Message):
    await message.answer("Свяжитесь с вашим руководителем через личные сообщения, @SCR1M1", reply_markup=create_keyboard())

async def remind_leaders():
    for student_id, student_info in topics["students"].items():
        if student_info["topic"] is None:
            await bot.send_message(ADMIN_ID, f"Студент {student_info['name']} еще не выбрал тему.")
    
    await bot.send_message(ADMIN_ID, "В вашей группе остались нераспределенные темы.")

async def main():
    await remind_leaders()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
