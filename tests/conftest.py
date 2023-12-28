import pytest

@pytest.fixture
def api_url():
    return "http://localhost:5000/"


@pytest.fixture
def api_url_v1(api_url):
    return api_url+"/api/v1"