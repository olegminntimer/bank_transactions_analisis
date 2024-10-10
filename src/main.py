import json
from pathlib import Path

from src.utils import import_xlsx, search_cards_number, search_cards_info

BASE_DIR = Path(__file__).resolve().parent.parent
file_name_log = str(BASE_DIR / "logs" / "main.log")

def main():
    file_xlsx = str(BASE_DIR / "data" / "operations.xlsx")
    transactions_main = import_xlsx(file_xlsx)

    cn = search_cards_number(transactions_main)
    print(cn)
    ts = search_cards_info(transactions_main, cn)
    print(ts)

    # path_to_file = str(BASE_DIR / "data" / "read_data.json")
    # with open(path_to_file, 'w') as f:
    #     f.write(str(transactions_main))


if __name__ == "__main__":
    main()
