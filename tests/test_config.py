"""The config is load-bearing, so it gets a test from day one."""

from bank_marketing.config import load_config, resolve


def test_config_exposes_the_business_assumptions():
    config = load_config()
    assert config["business"]["conversion_value"] > config["business"]["contact_cost"]
    assert config["capacity"]["contacts_available"] > 0


def test_raw_dataset_is_where_the_config_says_it_is():
    assert resolve(load_config()["data"]["raw_path"]).exists()
