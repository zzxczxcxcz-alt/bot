import csv
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

def import_themes_from_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                theme = row['Тема']
                leader = row['Руководитель']
                cmk = row['ЦМК']

                if validate_theme(theme) and validate_leader(leader) and validate_cmk(cmk): # type: ignore
                    cursor.execute('''
                    INSERT INTO themes (theme, leader, cmk)
                    VALUES (?, ?, ?)
                    ''', (theme, leader, cmk))
                    conn.commit()
                    logger.info(f"Тема '{theme}' успешно импортирована.")
                else:
                    logger.warning(f"Ошибка валидации для темы '{theme}': неверные данные.")
    except Exception as e:
        logger.error(f"Ошибка импорта тем: {e}")