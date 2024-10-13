from pandas import Timestamp

from src.reports import spending_by_category


def test_spending_by_category(test_df):
    """Тест вывода трат по категории"""
    new_df = spending_by_category(test_df, "Супермаркеты", "2021-12-31")
    sorted_list_category = new_df.to_dict(orient="records")
    assert sorted_list_category == [
        {"Дата операции": Timestamp('2021-12-31 16:44:00'), "Сумма операции": -160.89, "Категория": "Супермаркеты"},
        {"Дата операции": Timestamp('2021-12-31 16:42:04'), "Сумма операции": -64.00, "Категория": "Супермаркеты"},
        {"Дата операции": Timestamp('2021-12-31 16:39:04'), "Сумма операции": -118.12, "Категория": "Супермаркеты"},
        {"Дата операции": Timestamp('2021-11-19 18:54:29'), "Сумма операции": -339.90, "Категория": "Супермаркеты"},
    ]


def test_spending_by_category_with_incorrect_date(capsys, test_df):
    """Тест вывода сообщения при ошибке формата даты"""
    assert (spending_by_category(test_df, "Супермаркеты", "2022-12-31")).to_dict(orient="records") == []


def test_spending_by_category_with_incorrect_category(capsys, test_df):
    """Тест вывода сообщения при ошибке ввода категории"""
    assert (spending_by_category(test_df, "Супермаркет", "2021-12-31 14:46:24")).to_dict(orient="records") == []
