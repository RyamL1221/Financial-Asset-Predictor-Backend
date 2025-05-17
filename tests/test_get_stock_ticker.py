# tests/test_get_stock_ticker.py

import pytest
from flask import Flask, jsonify
import requests
from requests.exceptions import HTTPError

# import your blueprint
from src.routes.get_stock_ticker import get_stock_ticker_bp

# a dummy response class matching what your view expects
class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise HTTPError(f"{self.status_code} Error")

    def json(self):
        return self._json_data

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(get_stock_ticker_bp)
    app.testing = True
    return app.test_client()

def test_get_stock_ticker_success(monkeypatch, client):
    # stub out requests.get to return a 200
    fake = DummyResponse(200, {"ticker": "MSFT", "price": 300})
    monkeypatch.setattr(requests, "get",
        lambda url, headers, params, timeout: fake
    )

    resp = client.get("/get-stock-ticker/msft")
    assert resp.status_code == 200
    assert resp.get_json() == {"ticker": "MSFT", "price": 300}

def test_get_stock_ticker_http_error(monkeypatch, client):
    # stub out a 404 from Polygon
    fake = DummyResponse(404, {"error": "Not found"})
    monkeypatch.setattr(requests, "get",
        lambda url, headers, params, timeout: fake
    )

    resp = client.get("/get-stock-ticker/invalid")
    assert resp.status_code == 404
    body = resp.get_json()
    assert "error" in body
    assert "404 Error" in body["error"]

def test_get_stock_ticker_request_exception(monkeypatch, client):
    # stub out a network-level error
    def bad_get(*args, **kwargs):
        raise requests.RequestException("network down")
    monkeypatch.setattr(requests, "get", bad_get)

    resp = client.get("/get-stock-ticker/AAPL")
    assert resp.status_code == 502
    body = resp.get_json()
    assert body["error"].startswith("Error fetching data from Polygon API")
