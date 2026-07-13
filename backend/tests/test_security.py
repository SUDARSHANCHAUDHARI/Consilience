"""Security-control tests for the /api/query endpoint: input caps, rate limiting,
and optional bearer-token auth. These guard the expensive multi-model fan-out."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

import backend.main as main
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Each test starts with an empty rate-limit table and no auth token."""
    main._hits.clear()
    main.API_TOKEN = ""
    yield
    main._hits.clear()
    main.API_TOKEN = ""


def test_empty_query_rejected():
    r = client.post("/api/query", json={"query": "   "})
    assert r.status_code == 400


def test_oversized_query_rejected():
    main.MAX_QUERY_CHARS = 50
    r = client.post("/api/query", json={"query": "x" * 51})
    assert r.status_code == 413


@patch("backend.main.save_conversation")
@patch("backend.main.APIClient.call_model", new_callable=AsyncMock)
def test_rate_limit_returns_429(mock_call, _mock_save):
    mock_call.return_value = "ok"
    main.MAX_QUERY_CHARS = 8000
    main.RATE_MAX = 3
    codes = [client.post("/api/query", json={"query": "hi"}).status_code for _ in range(4)]
    assert codes[:3] == [200, 200, 200]
    assert codes[3] == 429


def test_missing_token_rejected_when_configured():
    main.API_TOKEN = "s3cret"
    r = client.post("/api/query", json={"query": "hi"})
    assert r.status_code == 401


def test_wrong_token_rejected():
    main.API_TOKEN = "s3cret"
    r = client.post("/api/query", json={"query": "hi"}, headers={"Authorization": "Bearer nope"})
    assert r.status_code == 401


@patch("backend.main.save_conversation")
@patch("backend.main.APIClient.call_model", new_callable=AsyncMock)
def test_correct_token_accepted(mock_call, _mock_save):
    mock_call.return_value = "ok"
    main.MAX_QUERY_CHARS = 8000
    main.RATE_MAX = 10
    main.API_TOKEN = "s3cret"
    r = client.post("/api/query", json={"query": "hi"}, headers={"Authorization": "Bearer s3cret"})
    assert r.status_code == 200
