import os

from growth_engine import mom_growth, is_flagged, validate_feed


def test_ethnic_wear_may_growth():
    growth = mom_growth(104520.77, 185107.61)

    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


def test_beauty_personal_care_june_growth():
    growth = mom_growth(35542.11, 37559.07)

    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


def test_exact_8_percent_boundary():
    growth = mom_growth(100000, 108000)

    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"


def test_corrupted_feed():
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "corrupted_feed.csv"
    )

    valid, errors = validate_feed(fixture_path)

    assert valid is False

    assert len(errors) == 3

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_monthly_category_feed():
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "monthly_category_revenue.csv"
    )

    valid, errors = validate_feed(fixture_path)

    assert valid is True
    assert errors == []