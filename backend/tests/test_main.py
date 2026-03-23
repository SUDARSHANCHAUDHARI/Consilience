import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["models"] > 0


# ---------------------------------------------------------------------------
# Query endpoint
# ---------------------------------------------------------------------------

def test_query_missing_body_returns_422():
    response = client.post("/api/query", json={})
    assert response.status_code == 422


@patch("backend.main.APIClient.call_model", new_callable=AsyncMock)
@patch("backend.main.save_conversation")
def test_query_returns_council_response(mock_save, mock_call):
    mock_call.return_value = "Test response"
    response = client.post("/api/query", json={"query": "What is 2+2?"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is 2+2?"
    assert len(data["stage1_responses"]) > 0
    assert len(data["stage2_reviews"]) > 0
    assert isinstance(data["stage3_final"], str)
    assert data["stage3_final"] == "Test response"
    mock_save.assert_called_once()


@patch("backend.main.APIClient.call_model", new_callable=AsyncMock)
@patch("backend.main.save_conversation")
def test_query_model_error_returns_error_marker(mock_save, mock_call):
    call_count = 0

    async def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("API unavailable")
        return "Response"

    mock_call.side_effect = side_effect
    response = client.post("/api/query", json={"query": "Test"})
    assert response.status_code == 200
    responses = response.json()["stage1_responses"]
    error_responses = [r for r in responses if r["response"].startswith("[Error:")]
    assert len(error_responses) >= 1


@patch("backend.main.APIClient.call_model", new_callable=AsyncMock)
@patch("backend.main.save_conversation")
def test_query_all_models_called(mock_save, mock_call):
    mock_call.return_value = "Response"
    response = client.post("/api/query", json={"query": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["stage1_responses"]) == len(data["stage2_reviews"])
