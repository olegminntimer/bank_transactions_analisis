import json
import logging
from calendar import monthrange
from datetime import datetime
from pathlib import Path

import pandas as pd

file_logs = str(Path(__file__).resolve().parent.parent / "logs" / "services.log")

logger_serv = logging.getLogger(__name__)
logger_serv.setLevel(logging.INFO)
handler_serv = logging.FileHandler(file_logs, mode='w')
formatter_serv = logging.Formatter("%(name)s %(asctime)s %(message)s")
handler_serv.setFormatter(formatter_serv )
logger_serv.addHandler(handler_serv )

def favorable_categories_of_increased_cashback(year: int, month: int, data: list ) -> str:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными для выбора
     в качестве категорий повышенного кэшбэка. Возвращает ответ в формате JSON"""
    logger_serv.info("Ищем выгодные категории повышенного кэшбэка")
    date_obj_start = datetime(year, month, 1, 0,0,0)
    date_obj_end = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
    date_string_start = date_obj_start.strftime("%d.%m.%Y %H:%M:%S")
    date_string_end = date_obj_end.strftime("%d.%m.%Y %H:%M:%S")
    df = pd.DataFrame(data)
    transaction_date = df.loc[
        df["Дата операции"].notnull() &
        (df["Дата операции"] >= date_string_start) &
        (df["Дата операции"] <= date_string_end) &
        (df["Сумма операции"] <= 0) &
        (df["Статус"] == "OK") &
        df["Кэшбэк"].notnull() &
        df["Категория"].notnull()
        ]
    df_group = transaction_date.groupby(["Категория"], as_index=False).agg({"Кэшбэк": "sum"})
    df_group["Кэшбэк"] = df_group["Кэшбэк"].apply(lambda x: round(x, 2))
    df_sorted_categories = df_group.sort_values(by=["Кэшбэк"], ascending=False)
    favor_cashback = df_sorted_categories[["Категория", "Кэшбэк"]].copy()[0:3]
    favor = {}
    for index, row in favor_cashback.iterrows():
        favor[row["Категория"]]= row["Кэшбэк"]
    logger_serv.info("Выгодные категории повышенного кэшбэка успешно найдены")
    return json.dumps(favor, ensure_ascii=False, indent=4)
