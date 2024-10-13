from pathlib import Path

from src.reports import spending_by_category
from src.services import favorable_categories_of_increased_cashback
from src.utils import import_xlsx
from src.views import home_page

BASE_DIR = Path(__file__).resolve().parent.parent
file_name_log = str(BASE_DIR / "logs" / "main.log")


def main() -> None:
    """Основная функция выводящая результат работы всех функций"""
    transactions = import_xlsx()
    date_str = input("\nВведите дату в формате: YYYY-MM-DD HH:MM:SS: ")
    print('На экран будет выведен JSON-ответ для веб-страницы "Главная":\n')
    print(home_page(date_str))
    print("\nНа экран будет выведен анализ выгодных категорий повышенного кэшбэка")
    year = input("Введите год для анализа в формате YYYY: ")
    month = input("Введите месяц для анализа в формате ММ: ")
    print(favorable_categories_of_increased_cashback(year, month, transactions))
    date_report = input(
        "\nВведите дату для отчета о тратах за последние" " три месяца от этой даты) в формате: YYYY-MM-DD: "
    )
    category = input(
        """Введите название категории для отчета о тратах
за последние три месяца (от ранее переданной даты): """
    )
    print(spending_by_category(transactions, category, date_report))


if __name__ == "__main__":
    main()
# 2020-04-15 00:00:00
