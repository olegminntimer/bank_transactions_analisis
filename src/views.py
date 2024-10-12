import json
import logging
from pathlib import Path

from src.utils import greeting, import_xlsx, transactions_date, get_user_settings, get_cards_info, \
    get_transaction_5_top, get_exchange_rate, get_stock_price

file_logs = str(Path(__file__).resolve().parent / "logs" / f"{__name__}.log")

logger_views = logging.getLogger(__name__)
logger_views.setLevel(logging.INFO)
handler_views = logging.FileHandler(file_logs, mode='w')
formatter_views = logging.Formatter("%(name)s %(asctime)s %(message)s")
handler_views.setFormatter(formatter_views)
logger_views.addHandler(handler_views)

def home_page(date: str) -> str:
    """Функция для страницы «Главная» принимает на вход строку с датой и временем
     в формате YYYY-MM-DD HH:MM:SS. Возвращает JSON-ответ."""
    logger_views.info("Функция для страницы «Главная»")
    transactions = import_xlsx()
    t_d = transactions_date(transactions, date)
    user_settings = get_user_settings()
    answer_json = {
        "greeting": greeting(),
        "cards": get_cards_info(t_d),
        "top transactions": get_transaction_5_top(t_d),
        "currency rates": get_exchange_rate(user_settings["user_currencies"]),
        "stock_prices": get_stock_price(user_settings["user_stocks"]),
    }
    logger_views.info("Функция для страницы «Главная» подготовила JSON-ответ")
    return json.dumps(answer_json, indent=4, ensure_ascii=False)
