import pandas as pd
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_csv(file_path, data):
    """Генерация CSV файла."""
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data[0].keys())
            for row in data:
                writer.writerow(row.values())
        logger.info(f"CSV файл '{file_path}' успешно сгенерирован.")
    except Exception as e:
        logger.error(f"Ошибка при генерации CSV файла: {e}")

def generate_excel(file_path, data):
    """Генерация Excel файла."""
    try:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        logger.info(f"Excel файл '{file_path}' успешно сгенерирован.")
    except Exception as e:
        logger.error(f"Ошибка при генерации Excel файла: {e}")

if __name__ == '__main__':
    sample_data = [
        {'ФИО': 'Иванов Иван Иванович', 'Телефон': '+1234567890', 'Группа': 'Группа 1'},
        {'ФИО': 'Петров Петр Петрович', 'Телефон': '+0987654321', 'Группа': 'Группа 2'},
    ]

    generate_csv('students.csv', sample_data)
    generate_excel('students.xlsx', sample_data)