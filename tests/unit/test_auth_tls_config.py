import certifi

from upstream.auth import AuthManager
from upstream.utils import ConfigManager


def test_auth_manager_uses_requests_ca_bundle_for_openapi_client(monkeypatch):
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
    auth_manager = AuthManager(config)

    assert auth_manager.configuration.verify_ssl is True
    assert auth_manager.configuration.ssl_ca_cert == certifi.where()


def test_auth_manager_uses_configured_ca_bundle_for_openapi_client():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
        ssl_ca_cert="/tmp/custom-ca.pem",
    )
    auth_manager = AuthManager(config)

    assert auth_manager.configuration.verify_ssl is True
    assert auth_manager.configuration.ssl_ca_cert == "/tmp/custom-ca.pem"


def test_auth_manager_can_disable_openapi_ssl_verification():
    config = ConfigManager(
        username="user",
        password="pass",
        base_url="https://upstreamapi.pods.portals.tapis.io",
        verify_ssl=False,
    )
    auth_manager = AuthManager(config)

    assert auth_manager.configuration.verify_ssl is False
