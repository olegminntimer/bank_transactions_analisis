from src.services import favorable_categories_of_increased_cashback
from tests.conftest import test_df


def test_favorable_categories_of_increased_cashback_inval_year(test_df):
    """Тест - введен неправильно год"""
    result_inval_year = favorable_categories_of_increased_cashback('202', '12', test_df)
    assert result_inval_year == '{}'


def test_favorable_categories_of_increased_cashback_inval_day(test_df):
    """Тест - введен неправильно деньд"""
    result_inval_day = favorable_categories_of_increased_cashback('2020', '13', test_df)
    assert result_inval_day == ''


