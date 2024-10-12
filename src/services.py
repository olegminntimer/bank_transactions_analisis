import json
import logging
from calendar import monthrange
import datetime
from pathlib import Path

import pandas as pd

file_logs = str(Path(__file__).resolve().parent.parent / "logs" / "services.log")

logger_serv = logging.getLogger(__name__)
logger_serv.setLevel(logging.INFO)
handler_serv = logging.FileHandler(file_logs, mode='w')
formatter_serv = logging.Formatter("%(name)s %(asctime)s %(message)s")
handler_serv.setFormatter(formatter_serv )
logger_serv.addHandler(handler_serv )

def favorable_categories_of_increased_cashback(year: str, month: str, data: list ) -> str:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными для выбора
     в качестве категорий повышенного кэшбэка. Возвращает ответ в формате JSON"""
    logger_serv.info("Ищем выгодные категории повышенного кэшбэка")
    try:
        date_obj_start = datetime.datetime(int(year), int(month), 1, 0,0,0).date()
        date_obj_end = datetime.datetime(int(year), int(month), monthrange(int(year), int(month))[1], 23, 59, 59).date()
        date_string_start = date_obj_start.strftime("%d.%m.%Y %H:%M:%S")
        date_string_end = date_obj_end.strftime("%d.%m.%Y %H:%M:%S")
    except ValueError:
        logger_serv.error("Некорректный формат даты")
        return None
    df = pd.DataFrame(data)
    df_copy = df[["Дата операции", "Сумма операции", "Статус", "Кэшбэк", "Категория"]].copy()
    df_copy["Дата операции"] = df_copy["Дата операции"].apply(
        lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
    )
    # print(df_copy)
    transaction_date = df_copy.loc[
        (df_copy["Дата операции"] >= date_obj_start) &
        (df_copy["Дата операции"] <= date_obj_end) &
        (df_copy["Сумма операции"] <= 0) &
        (df_copy["Статус"] == "OK") &
        df_copy["Кэшбэк"].notnull() &
        df_copy["Категория"].notnull()
        ]
    # print(transaction_date)
    df_group = transaction_date.groupby(["Категория"], as_index=False).agg({"Кэшбэк": "sum"})
    df_group["Кэшбэк"] = df_group["Кэшбэк"].apply(lambda x: round(x, 2))
    df_sorted_categories = df_group.sort_values(by=["Кэшбэк"], ascending=False)
    favor_cashback = df_sorted_categories[["Категория", "Кэшбэк"]].copy()
    favor = {}
    for index, row in favor_cashback.iterrows():
        favor[row["Категория"]]= row["Кэшбэк"]
    logger_serv.info("Выгодные категории повышенного кэшбэка успешно найдены")
    return json.dumps(favor, ensure_ascii=False, indent=4)
