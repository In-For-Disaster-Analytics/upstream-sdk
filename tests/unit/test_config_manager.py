from upstream.utils import ConfigManager


def test_config_manager_normalizes_pods_web_host_to_api_host():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstream.pods.tacc.tapis.io/",
    )

    assert config.base_url == "https://upstreamapi.pods.tacc.tapis.io"


def test_config_manager_keeps_api_host():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.tacc.tapis.io",
    )

    assert config.base_url == "https://upstreamapi.pods.tacc.tapis.io"
