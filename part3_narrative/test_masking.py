from masking import alias_for, assert_no_raw_names_leak


def test_alias_for_rs019():
    assert alias_for("RS019") == "ALIAS-19"


def test_alias_for_rs006():
    assert alias_for("RS006") == "ALIAS-06"


def test_raw_name_is_detected():
    text = "West - Mumbai Reseller 1 generated high revenue."

    assert assert_no_raw_names_leak(
        text,
        ["Mumbai Reseller 1"]
    ) is False


def test_masked_narrative_has_no_raw_name():
    text = "West - ALIAS-19 generated high revenue."

    assert assert_no_raw_names_leak(
        text,
        ["Mumbai Reseller 1"]
    ) is True