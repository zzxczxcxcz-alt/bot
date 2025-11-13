import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8137628454:AAEUPW8fKH3Jg7Edl47gME46MHEENk6RFZQ"
 # pyright: ignore[reportUndefinedVariable]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("Кнопка 1", callback_data='button1')
    button_2 = InlineKeyboardButton("Кнопка 2", callback_data='button2')
    keyboard.add(button_1, button_2)
    await message.reply("Привет! Нажми на кнопку:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_button(callback_query: types.CallbackQuery):
    code = callback_query.data
    if code == 'button1':
        await bot.answer_callback_query(callback_query.id, text='Вы нажали на Кнопку 1')
    elif code == 'button2':
        await bot.answer_callback_query(callback_query.id, text='Вы нажали на Кнопку 2')