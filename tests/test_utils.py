from unittest.mock import patch

import pandas as pd

from src.utils import greeting, get_exchange_rate, get_cards_info, get_transaction_5_top
from freezegun import freeze_time

from tests.conftest import test_df


def test_greeting():
    """Тест вывода приветсвия в зависимости от текущего времени"""
    with freeze_time("2024-09-30 16:39:11"):
        assert greeting() == "Добрый день"
    with freeze_time("2024-09-30 08:39:11"):
        assert greeting() == "Доброе утро"
    with freeze_time("2024-09-30 19:39:11"):
        assert greeting() == "Добрый вечер"
    with freeze_time("2024-09-30 03:39:11"):
        assert greeting() == "Доброй ночи"



def test_get_cards_info(test_df):
    """Тест корректности работы функции get_cards_info"""
    assert get_cards_info(test_df, "2021-12-31 16:44:00") == [
        # {"last_digits": "4556", "total_spent": 1020.9, "cashback": 10.21},
        {"last_digits": "5091", "total_spent": 1589.0, "cashback": 15.89},
        {"last_digits": "7197", "total_spent": 344.33, "cashback": 3.44}
    ]


def test_get_cards_info_incorrect_date_format(test_df):
    """Тест функции с некорректным форматом даты"""
    assert get_cards_info(test_df, "2022-12-31 16:44:00") == []


def test_top_5_transactions(test_df):
    """Тест топ 5 транзакций за месяц"""
    assert get_transaction_5_top(test_df, "2021-12-31 16:44:00") == [
        {"date": "31.12.2021", "amount": -564.0, "category": "Различные товары", "description": "Константин. К"},
        {"date": "09.12.2021", "amount": -525.0, "category": "Одежда и обувь", "description": "WILDBERRIES"},
        {"date": "16.12.2021", "amount": -500.0, "category": "Местный транспорт", "description": "Метро Санкт-петербург"},
        {"date": "31.12.2021", "amount": -160.89, "category": "Супермаркеты", "description": "Колхоз"},
        {"date": "31.12.2021", "amount": -118.12, "category": "Супермаркеты", "description": "Магнит"},
    ]


def test_top_5_transactions_with_incorrect_date_format(test_df):
    """Тест топа транзакций при некорректном формате даты"""
    assert get_transaction_5_top(test_df, "2023-12-31 16:44:00") == []


@patch("src.utils.requests.get")
def test_get_exchange_rate(mock_get, currencies, answer_currencies):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 200
    assert get_exchange_rate(currencies) == [{"currency": "USD", "rate": 92.86}]


@patch("src.utils.requests.get")
def test_get_exchange_rate_with_incorrect_status_code(mock_get, currencies, answer_currencies):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 404
    assert get_exchange_rate(currencies) == []

