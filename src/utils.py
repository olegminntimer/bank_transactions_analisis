import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=str(BASE_DIR / "logs" / "utils.log"),
    filemode="w",
    encoding="utf-8",
)
logger_xlsx = logging.getLogger("xlsx")
logger_greeting = logging.getLogger("greeting")


def import_xlsx(file_name: str) -> list:
    """Функция считывает финансовые операции из excel-файла и выдает список словарей с транзакциями"""
    logger_xlsx.debug("Открываем excel-файл для чтения")
    try:
        reader_excel = pd.read_excel(file_name)
        logger_xlsx.debug("Считали excel")
    except FileNotFoundError:
        logger_xlsx.error("Файл excel не найден")
        return []
    return reader_excel.to_dict(orient="records")


def greeting_str() -> str:
    ''' Функция возвращает приветствие в зависимости от текущего времени суток '''
    current_time = datetime.now().time()
    t00 = datetime.strptime('00:00:00', '%H:%M:%S').time() #     Ночь: с 22:00 по 4:59.
    t05 = datetime.strptime('05:00:00', '%H:%M:%S').time() #     Утро: с 5:00 по 11:59.
    t12 = datetime.strptime('12:00:00', '%H:%M:%S').time() #     День: с 12:00 по 16:59.
    t17 = datetime.strptime('17:00:00', '%H:%M:%S').time() #     Вечер: с 17:00 по 21:59.
    t22 = datetime.strptime('22:00:00', '%H:%M:%S').time()
    t24 = datetime.strptime('23:59:59', '%H:%M:%S').time()

    if (t00 <= current_time < t05) or (t22 <= current_time < t24):
        logger_greeting.info("Доброй ночи")
        return "Доброй ночи"
    elif t05 <= current_time < t12:
        logger_greeting.info("Доброе утро")
        return "Доброе утро"
    elif t12 <= current_time < t17:
        logger_greeting.info("Добрый день")
        return "Добрый день"
    elif t17 <= current_time < t22:
        logger_greeting.info("Добрый вечер")
        return "Добрый вечер"


def search_cards_number(transactions: list) -> list:
    ''' Функция создает и сортирует по возрастанию список с номерами карт из списка транзакций '''
    cards_number = []
    for transaction in transactions:
        card_num = transaction["Номер карты"]
        if (type(card_num) == str) and (card_num not in cards_number):
            cards_number.append(card_num)
    cards_number.sort()
    return cards_number


def search_cards_info(transactions: list, cards_numbers: list) -> list:
    ''' Функция возвращает список словарей с краткой информацией по каждой карте '''
    cards_info = []
    # cards_numbers = search_cards_number(transactions)
    for number in cards_numbers:
        summ = 0
        for transaction in transactions:
            if transaction["Номер карты"] == number:
                summ += transaction["Сумма операции с округлением"]
        cards_info.append({"last_digits": number[-4:], "total_spent": round(summ, 2), "cashback": round(summ/100, 2)})
    return cards_info