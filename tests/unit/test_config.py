from passportpal.config import Settings


def test_settings_default_values():
    settings = Settings(app_env="ci")

    assert settings.app_env == "ci"
    assert settings.app_name == "passportpal"
    assert settings.data_file is not None
