import pytest
from ..dates import int_to_short_month_name

class TestDates:
    def test_converts_months_to_strings(self):
        assert int_to_short_month_name(0) == 'JAN'
        assert int_to_short_month_name(1) == 'FEB'
        assert int_to_short_month_name(2) == 'MAR'
        assert int_to_short_month_name(3) == 'APR'
        assert int_to_short_month_name(4) == 'MAY'
        assert int_to_short_month_name(5) == 'JUN'
        assert int_to_short_month_name(6) == 'JUL'
        assert int_to_short_month_name(7) == 'AUG'
        assert int_to_short_month_name(8) == 'SEP'
        assert int_to_short_month_name(9) == 'OCT'
        assert int_to_short_month_name(10) == 'NOV'
        assert int_to_short_month_name(11) == 'DEC'

    def test_when_out_of_range_it_raises_exception(self):
        with pytest.raises(Exception):
            int_to_short_month_name(12)
            int_to_short_month_name(0)
