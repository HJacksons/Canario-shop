import pytest
from fastapi.testclient import TestClient
from main import app, memcache_client


client = TestClient(app)


def test_shop_homepage_status_code():
    """
    Test if the homepage returns a 200 OK status code.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_invalidate_cache():
    """
    Test if the cache invalidation endpoint works.
    """
    response = client.post("/invalidate_cache")
    if memcache_client:  # If using memcache
        assert response.json() == {"status": "cache invalidated"}
    else:
        assert response.json() == {"status": "memcache not used"}


def test_shop_homepage_content():
    """
    Test if the homepage contains the expected content.
    """
    response = client.get("/")
    assert "Canario Shop" in response.text
    assert "Your one-stop shop for all things Canario." in response.text
    assert "Categories" in response.text
    assert "hourly_promotion" in response.text
    assert "END OF COUNT UNTIL CHRISTMAS OFFER " in response.text
    # ... add more content assertions as needed


if __name__ == "__main__":
    pytest.main()
