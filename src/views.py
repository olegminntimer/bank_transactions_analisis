import json

from src.utils import greeting, import_xlsx, transactions_date, get_user_settings, get_cards_info, \
    get_transaction_5_top, get_exchange_rate, get_stock_price


def home_page(date: str):
    """Функция для страницы «Главная» принимает на вход строку с датой и временем
     в формате YYYY-MM-DD HH:MM:SS. Возвращает JSON-ответ."""
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
    # answer_in_json_format = json.dumps(answer_json, indent=4, ensure_ascii=False)
    return json.dumps(answer_json, indent=4, ensure_ascii=False)
