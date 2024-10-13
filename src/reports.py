import datetime
import logging
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional
from pandas.io.formats.style import Styler
import pandas as pd
from dateutil.relativedelta import relativedelta

file_logs = str(Path(__file__).resolve().parent.parent / "logs" / "reports.log")

logger_rep = logging.getLogger(__name__)
logger_rep.setLevel(logging.INFO)
handler_rep = logging.FileHandler(file_logs, mode="w")
formatter_rep = logging.Formatter("%(name)s %(asctime)s %(message)s")
handler_rep.setFormatter(formatter_rep)
logger_rep.addHandler(handler_rep)


def report_write(filename: str = "report") -> Callable:
    """Декоратор с параметром — принимает имя файла в качестве параметра. Декоратор без параметра
    — записывает данные отчета в файл с названием по умолчанию"""

    def my_decorator(function: Callable) -> Callable:
        """Декоратор записи данных в файл"""

        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Функция - обёртка"""
            result = function(*args, **kwargs)
            filename_full = str(Path(__file__).resolve().parent.parent / "data" / f"{filename}.json")
            result.to_json(path_or_buf=filename_full, orient="records", indent=4, force_ascii=False)
            return result

        return inner

    return my_decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    logger_rep.info("Создаем отчет о тратах по заданной категории")
    df_copy = transactions[["Дата операции", "Сумма операции", "Категория"]].copy()
    try:
        logger_rep.info(f"Создадим интервал")
        if date:
            date_obj_end = datetime.datetime.strptime(date, "%Y-%m-%d")
            date_obj_end = date_obj_end.replace(hour=23, minute=59, second=59)
            date_obj_start = date_obj_end - relativedelta(months=3)
            logger_rep.info(f"Создан интервал от {date_obj_start} до {date_obj_end}")
        else:
            date_obj_end = datetime.datetime.now()
            date_obj_end = date_obj_end.replace(hour=23, minute=59, second=59)
            date_obj_start = date_obj_end - relativedelta(months=3)
            logger_rep.info(f"Создан интервал от {date_obj_start} до {date_obj_end}")
        logger_rep.info("Конвертируем столбец 'Дата операции' из строки в объект")
        df_copy["Дата операции"] = df_copy["Дата операции"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S")
        )
        logger_rep.info("Сконвертировали столбец 'Дата операции' из строки в объект")
        logger_rep.info(f"Выберем операции в заданном интервале и где есть выбранная категория {category}")
        df_report = df_copy.loc[
            (df_copy["Дата операции"] >= date_obj_start)
            & (df_copy["Дата операции"] <= date_obj_end)
            & (df_copy["Категория"] == category)
        ]
        logger_rep.info(f"Выбрали операции в заданном интервале и где есть выбранная категория '{category}'")
        # df_report.loc[:, "Дата операции"] = df_report["Дата операции"].apply(lambda x: x.strftime("%d.%m.%Y"))
        # df_report["Дата операции"] = pd.to_datetime(df_report["Дата операции"].astype(str), format="%d.%m.%Y")
        # df_report["Дата операции2"] = df_report["Дата операции"].dt.strftime("%d.%m.%Y")
        # df_report = df_copy.loc[df_report["Дата операции"].strftime("%d.%m.%Y")]
        # df_report["Дата операции"] = df_report["Дата операции"].astype(str)
        # df_report["Дата операции"] = df_report["Дата операции"].dt.strftime("%d.%m.%Y")
        # df_copy.loc["Дата операции"] = df_report.style.format({"Дата операции": lambda t: t.strftime("%d.%m.%Y %H:%M:%S")})
        # df_report.style.format({"Дата операции": lambda t: t.strftime("%d.%m.%Y")})

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
