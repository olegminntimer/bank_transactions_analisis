import pandas as pd


def import_xlsx(filename: str) -> list:
    """Функция считывает финансовые операции из excel-файла и выдает список словарей с транзакциями"""
    # logger_csv.debug("Открываем excel-файл для чтения")
    try:
        reader_excel = pd.read_excel(filename)
        # logger_xlsx.debug("Считали excel")
    except FileNotFoundError:
        # logger_xlsx.error("Файл excel не найден")
        return []
    return reader_excel.to_dict(orient="records")
