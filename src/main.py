from pathlib import Path

from src.read_data import import_xlsx


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_name = str(BASE_DIR / "data" / "operations.xlsx")
    transactions_main = import_xlsx(file_name)


if __name__ == "__main__":
    main()
