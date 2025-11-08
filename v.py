import datetime
import re
import matplotlib.pyplot as plt
from aiogram import types
from aiogram.fsm.context import FSMContext
from db.database import cursor, conn # type: ignore
from fsm.states import Registration # type: ignore
from ui.keyboards import get_main_keyboard # type: ignore
from handlers import router # type: ignore # type: ignore


def get_distribution_statistics():
    try:
        cursor.execute('''
        SELECT group_name, COUNT(*) as total_students, SUM(hours_missed) as total_hours_missed
        FROM attendances
        GROUP BY group_name
        ''')
        return cursor.fetchall()  # Возвращает статистику по группам
    except Exception as e:
        logger.error(f"Ошибка при получении статистики распределения: {e}") # type: ignore
        return []


def visualize_distribution_statistics(statistics):
    groups = [row[0] for row in statistics]
    total_students = [row[1] for row in statistics]
    total_hours_missed = [row[2] for row in statistics]

    plt.figure(figsize=(10, 6))

    plt.bar(groups, total_students, color='skyblue', label='Общее количество студентов', alpha=0.7)
    plt.bar(groups, total_hours_missed, color='salmon', label='Общее количество пропусков', alpha=0.7)

    plt.xlabel('Группы')
    plt.ylabel('Количество')
    plt.title('Статистика распределения по группам')
    plt.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('distribution_statistics.png')
    plt.close()


@router.message(commands=['view_distribution_statistics'])
async def view_distribution_statistics(message: types.Message):
    statistics = get_distribution_statistics()
    if not statistics:
        await message.answer("❌ Нет данных для отображения.")
        return

    visualize_distribution_statistics(statistics)  # Генерируем график
    await message.answer("📊 Вот график статистики распределения:", reply_markup=get_main_keyboard('curator'))

    with open('distribution_statistics.png', 'rb') as photo:
        await message.answer_photo(photo=photo, caption="Статистика распределения по группам.")