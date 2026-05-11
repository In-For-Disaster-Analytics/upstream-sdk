import certifi

from upstream.utils import ConfigManager


def test_config_manager_normalizes_pods_web_host_to_api_host():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstream.pods.portals.tapis.io/",
    )

    assert config.base_url == "https://upstreamapi.pods.portals.tapis.io"


def test_config_manager_keeps_api_host():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
    )

    assert config.base_url == "https://upstreamapi.pods.portals.tapis.io"


def test_config_manager_defaults_to_certifi_ca_bundle(monkeypatch):
    for env_name in (
        "UPSTREAM_SSL_CA_CERT",
        "REQUESTS_CA_BUNDLE",
        "CURL_CA_BUNDLE",
        "SSL_CERT_FILE",
    ):
        monkeypatch.delenv(env_name, raising=False)

    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
    )

    assert config.ssl_ca_cert == certifi.where()
    assert config.request_verify == certifi.where()


def test_config_manager_uses_explicit_ca_bundle():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
        ssl_ca_cert="/tmp/custom-ca.pem",
    )

    assert config.ssl_ca_cert == "/tmp/custom-ca.pem"
    assert config.request_verify == "/tmp/custom-ca.pem"


def test_config_manager_reads_ca_bundle_from_environment(monkeypatch):
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/tmp/requests-ca.pem")

    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
    )

    assert config.ssl_ca_cert == "/tmp/requests-ca.pem"
    assert config.request_verify == "/tmp/requests-ca.pem"


def test_config_manager_can_disable_ssl_verification():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
        verify_ssl=False,
    )

    assert config.verify_ssl is False
    assert config.request_verify is False
