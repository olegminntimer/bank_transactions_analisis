import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных из .env-файла
load_dotenv()
alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
api_key = os.getenv("APILAYER_API_KEY")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    filename=str(BASE_DIR / "logs" / "utils.log"),
    filemode="w",
    encoding="utf-8",
)
logger_xlsx = logging.getLogger("xlsx")
logger_greeting = logging.getLogger("greeting")
logger_cards_number = logging.getLogger("cards_number")
logger_cards_info = logging.getLogger("cards_info")
logger_top_5 = logging.getLogger("Top-5")
logger_us_set = logging.getLogger("user_settings")
logger_exchange_rate = logging.getLogger("exchange_rate")
logger_stock_price = logging.getLogger("stock_price")



def import_xlsx() -> pd.DataFrame:
    """Функция считывает финансовые операции из excel-файла и выдает DataFrame с транзакциями"""
    try:
        logger_xlsx.debug("Открываем excel-файл для чтения")
        file_xlsx = str(BASE_DIR / "data" / "operations.xlsx")
        reader_excel = pd.read_excel(file_xlsx)
        logger_xlsx.debug("Считали excel")
    except FileNotFoundError:
        logger_xlsx.error("Файл excel не найден")
        return []
    return reader_excel


def greeting() -> str:
    """Функция возвращает приветствие в зависимости от текущего времени суток"""
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


def transactions_date(data_frame: pd.DataFrame, date: str) -> pd.DataFrame:
    """Функция возвращает DataFrame данные с начала месяца,
     на который выпадает входящая дата, по входящую дату, со статусом 'OK'"""
    df = data_frame
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_string = date_obj.strftime("%d-%m-%Y %H:%M:%S")
    date_obj_start = date_obj.replace(day=1, hour=0, minute=0, second=0)
    date_string_start = date_obj_start.strftime("%d-%m-%Y %H:%M:%S")
    transaction_date = df.loc[
        df["Дата операции"].notnull() &
        (df["Дата операции"] >= date_string_start) &
        (df["Дата операции"] <= date_string) &
        (df["Сумма операции"] <= 0) &
        (df["Статус"] == "OK")
        ]
    return transaction_date

def get_cards_info(data_frame: pd.DataFrame) -> list:
    """Функция возвращает список словарей с краткой информацией по каждой карте в отчетный период"""
    try:
        logger_cards_info.info("Создаем список словарей с краткой информацией по каждой карте")
        df = data_frame
        df_filtered = df.loc[df["Номер карты"].notnull()]
        df_group = df_filtered.groupby(["Номер карты"], as_index=False).agg({"Сумма операции с округлением": "sum"})
        df_group["Кэшбэк"] = df_group["Сумма операции с округлением"].apply(lambda x: round(abs(x) / 100, 2))
        df_group["Номер карты"] = df_group["Номер карты"].apply(lambda x: x.replace("*", ""))
        df_group.rename(columns={"Номер карты": "last_digits", "Сумма операции с округлением": "total_spent", "Кэшбэк": "cashback"}, inplace=True)
        df_group["total_spent"] = df_group["total_spent"].apply(lambda x: round(x, 2))
        data_list = df_group.to_dict(orient="records")
        logger_cards_info.info("Информация по картам собрана")
        return data_list
    except ValueError:
        logger_cards_info.error("Ошибка ввода данных: неверный формат даты")
        return []


def get_transaction_5_top(data_frame: pd.DataFrame) -> list:
    """Функция возвращает список топ 5 транзакций по сумме платежа со статусом 'OK'"""
    df = data_frame
    df_sorted_amount = df.sort_values(
        by=["Сумма операции"], ascending=False, key=lambda x: abs(x)
    )
    transaction_5_top = df_sorted_amount[0:5]
    data_list = []
    for index, row in transaction_5_top.iterrows():
        data_dict = {
            "date": datetime.strptime(row["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y"),
            "amount": round(row["Сумма операции"], 2),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        data_list.append(data_dict)
    return data_list


def get_user_settings() -> dict:
    """
    Функция считывает из файла пользовательских настроек словарь валют
    и акций, которые будут отображены на веб-страницах. Возвращает словарь.
    """
    file_settings = str(BASE_DIR / "data" / "user_settings.json")
    with open(file_settings) as f:
        data = json.load(f)
    logger_us_set.info("Считали файл настроек")
    return data


def get_exchange_rate(currencies: list) -> list:
    """Функция возвращает курс валют"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{api_key}"}
    exchange_rates = []
    for currency in currencies:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        logger_exchange_rate.debug("Делаем запрос курса валют")
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            ex_r = response.json()
            currency_rate = {"currency": f"{ex_r["base"]}", "rate": round(float(ex_r["rates"]["RUB"]), 2)}
            exchange_rates.append(currency_rate)
            logger_exchange_rate.debug("Запрос - успешно")
        else:
            logger_exchange_rate.warning("Запрос не прошёл")
            return []
    return exchange_rates



def get_stock_price(stocks: list) -> list:
    """Функция возвращает список стоимости акций из S&P500"""
    logger_stock_price.debug("Запрашиваем стоимость акций")
    stocks_price = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={alpha_key}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            date = res["Meta Data"]["3. Last Refreshed"]
            new_dict = {"stock": stock, "price": round(float(res["Time Series (Daily)"][f"{date}"]["2. high"]), 2)}
            stocks_price.append(new_dict)
            logger_stock_price.info("Стоимость акций - запрос успешен")
        else:
            logger_stock_price.error("Ошибка запроса стоимости акций")
    return stocks_price
