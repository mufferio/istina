from istina.config.settings import load_settings

def test_settings_loads():
    from istina.config.settings import load_settings
    s = load_settings()
    assert s.env == "dev"