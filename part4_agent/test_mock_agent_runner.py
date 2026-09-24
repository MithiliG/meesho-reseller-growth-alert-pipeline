import json
import os

from mock_agent_runner import run

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def fixture(name):
    return os.path.join(BASE_DIR, "fixtures", name)

def test_may_scenario():
    result = run(
        "May",
        fixture("april.csv"),
        fixture("may.csv"),
    )

    assert result["validation_status"] == "valid"

    assert [
        item["category"]
        for item in result["flagged_categories"]
    ] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]

    assert [
        item["mom_pct"]
        for item in result["flagged_categories"]
    ] == [
        77.1,
        -23.6,
        -23.48,
    ]

    assert all(
        item["drafted"] is True
        for item in result["flagged_categories"]
    )

    assert set(result["suppressed_categories"]) == {
        "Beauty & Personal Care",
        "Home & Kitchen",
    }

    assert result["escalated_categories"] == []

def test_june_scenario():
    result = run(
        "June",
        fixture("may.csv"),
        fixture("june.csv"),
    )

    assert result["validation_status"] == "valid"

    assert [
        item["category"]
        for item in result["flagged_categories"]
    ] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]

    assert [
        item["mom_pct"]
        for item in result["flagged_categories"]
    ] == [
        -58.74,
        42.59,
        23.9,
    ]

    assert result["suppressed_categories"] == [
        "Western Wear"
    ]

    assert "Beauty & Personal Care" not in [
        item["category"]
        for item in result["flagged_categories"]
    ]

    assert "Beauty & Personal Care" not in result[
        "suppressed_categories"
    ]

    assert result["escalated_categories"] == []

def test_corrupted_feed_hard_stop():
    result = run(
        "July",
        fixture("may.csv"),
        os.path.join(
            BASE_DIR,
            "..",
            "part2_engine",
            "fixtures",
            "corrupted_feed.csv",
        ),
    )

    assert result["validation_status"] == "invalid"

    assert result["action_taken"] == "hard_stop"

    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert result["flagged_categories"] == []

    assert result["suppressed_categories"] == []

def test_exact_boundary():
    result = run(
        "Test2",
        fixture("boundary_previous.csv"),
        fixture("boundary_current.csv"),
    )

    assert result["flagged_categories"] == []

    assert result["escalated_categories"] == [
        "Boundary Category"
    ]

def test_messages_contain_required_numbers():
    result = run(
        "May",
        fixture("april.csv"),
        fixture("may.csv"),
    )

    for item in result["flagged_categories"]:
        message = item["message"]

        assert item["category"] in message
        assert str(item["mom_pct"]) in message