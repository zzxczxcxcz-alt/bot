import csv
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

def import_students_from_csv(file_path):
    """Импорт студентов из CSV файла."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                full_name = row['ФИО']
                phone = row.get('Телефон', '')
                telegram = row.get('Telegram', '')
                group = row.get('Группа', '')

                if validate_student(full_name):
                    cursor.execute('''
                    INSERT INTO students (name, phone, telegram, group_name)
                    VALUES (?, ?, ?, ?)
                    ''', (full_name, phone, telegram, group))
                    conn.commit()
                    logger.info(f"Студент '{full_name}' успешно добавлен в группу '{group}'.")
                else:
                    logger.warning(f"Ошибка валидации для студента '{full_name}': неверные данные.")
    except Exception as e:
        logger.error(f"Ошибка импорта студентов: {e}")

def import_students_from_excel(file_path):
    """Импорт студентов из Excel файла."""
    try:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            full_name = row['ФИО']
            phone = row.get('Телефон', '')
            telegram = row.get('Telegram', '')
            group = row.get('Группа', '')

            if validate_student(full_name):
                cursor.execute('''
                INSERT INTO students (name, phone, telegram, group_name)
                VALUES (?, ?, ?, ?)
                ''', (full_name, phone, telegram, group))
                conn.commit()
                logger.info(f"Студент '{full_name}' успешно добавлен в группу '{group}'.")
            else:
                logger.warning(f"Ошибка валидации для студента '{full_name}': неверные данные.")
    except Exception as e:
        logger.error(f"Ошибка импорта студентов: {e}")

def validate_student(full_name):
    """Простая валидация для имени студента."""
    return len(full_name.strip()) > 0

if __name__ == '__main__':
    import_students_from_csv('students.csv')
    import_students_from_excel('students.xlsx')
    conn.close()