from pathlib import Path

from src.views import home_page


BASE_DIR = Path(__file__).resolve().parent.parent
file_name_log = str(BASE_DIR / "logs" / "main.log")

def main():
    # hp = home_page("2019-10-20 23:00:00")
    # print(hp)
    pass


if __name__ == "__main__":
    main()
