import logging
import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

file_logs = str(Path(__file__).resolve().parent.parent / "logs" / "reports.log")

logger_rep = logging.getLogger(__name__)
logger_rep.setLevel(logging.INFO)
handler_rep = logging.FileHandler(file_logs, mode='w')
formatter_rep = logging.Formatter("%(name)s %(asctime)s %(message)s")
handler_rep.setFormatter(formatter_rep )
logger_rep.addHandler(handler_rep )

def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    logger_rep.info("Создаем отчет о тратах по заданной категории")
    df_copy = transactions[["Дата операции", "Сумма операции", "Категория"]].copy()
    try:
        if date:
            date_obj_end = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            date_obj_start = date_obj_end - relativedelta(months=3)
        else:
            date_obj_end = datetime.datetime.now().date()
            date_obj_start = date_obj_end - relativedelta(months=3)
        df_copy["Дата операции"] = df_copy["Дата операции"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        df_report = df_copy.loc[
            (df_copy["Дата операции"] >= date_obj_start) &
            (df_copy["Дата операции"] <= date_obj_end) &
            (df_copy["Категория"] == category)
        ]
        df_report.loc[:, "Дата операции"] = df_report["Дата операции"].apply(lambda x: x.strftime("%d.%m.%Y"))
        if not df_report.to_dict(orient="records"):
            raise NameError
    except ValueError:
        logger_rep.error("Некорректный формат даты")
        return pd.DataFrame({})
    except NameError:
        logger_rep.error("Неверно введена категория")
        return pd.DataFrame({})
    else:
        logger_rep.info("Выборка операций успешно завершена")
        return df_report
    finally:
        logger_rep.info("Формирование отчёта завершено")
