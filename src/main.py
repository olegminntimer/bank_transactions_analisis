from pathlib import Path

import pandas as pd

from src.reports import spending_by_category
from src.services import favorable_categories_of_increased_cashback
from src.utils import import_xlsx
# from src.views import home_page


BASE_DIR = Path(__file__).resolve().parent.parent
file_name_log = str(BASE_DIR / "logs" / "main.log")

def main():
    # hp = home_page("2019-10-20 23:00:00")
    # print(hp)
    tr = import_xlsx()
    # fv = favorable_categories_of_increased_cashback("2020","1",tr)
    # print(fv)
    tr_df = pd.DataFrame(tr)
    sc = spending_by_category(tr_df, "Аптеки", "2020-08-07 00:00:00")
    print(sc)


if __name__ == "__main__":
    main()
