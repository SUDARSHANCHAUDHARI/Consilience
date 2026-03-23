import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from backend.api_clients import (
    APIClient, AnthropicClient, OpenAIClient,
    GoogleClient, XAIClient, MetaClient, MistralClient,
)


def mock_response(json_data, status_code=200):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

class TestAPIClientRouting:
    async def test_routes_to_anthropic(self, mocker):
        m = mocker.patch.object(AnthropicClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("anthropic/claude-opus-4-5", "hi")
        m.assert_called_once_with("anthropic/claude-opus-4-5", "hi", "")

    async def test_routes_to_openai(self, mocker):
        m = mocker.patch.object(OpenAIClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("openai/gpt-4o", "hi")
        m.assert_called_once()

    async def test_routes_to_google(self, mocker):
        m = mocker.patch.object(GoogleClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("google/gemini-2.0-flash", "hi")
        m.assert_called_once()

    async def test_routes_to_xai(self, mocker):
        m = mocker.patch.object(XAIClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("xai/grok-beta", "hi")
        m.assert_called_once()

    async def test_routes_to_meta(self, mocker):
        m = mocker.patch.object(MetaClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("meta/llama-3.1-70b-instruct", "hi")
        m.assert_called_once()

    async def test_routes_to_mistral(self, mocker):
        m = mocker.patch.object(MistralClient, "call", new_callable=AsyncMock, return_value="ok")
        await APIClient.call_model("mistral/mistral-large", "hi")
        m.assert_called_once()

    async def test_unknown_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown model provider"):
            await APIClient.call_model("unknown/model", "hi")


# ---------------------------------------------------------------------------
# API key validation
# ---------------------------------------------------------------------------

class TestAPIKeyValidation:
    async def test_anthropic_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY is not set"):
            await AnthropicClient.call("anthropic/claude-opus-4-5", "hi")

    async def test_openai_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
            await OpenAIClient.call("openai/gpt-4o", "hi")

    async def test_google_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        with pytest.raises(ValueError, match="GOOGLE_API_KEY is not set"):
            await GoogleClient.call("google/gemini-2.0-flash", "hi")

    async def test_xai_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("XAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="XAI_API_KEY is not set"):
            await XAIClient.call("xai/grok-beta", "hi")

    async def test_together_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("TOGETHER_API_KEY", raising=False)
        with pytest.raises(ValueError, match="TOGETHER_API_KEY is not set"):
            await MetaClient.call("meta/llama-3.1-70b-instruct", "hi")

    async def test_mistral_missing_key_raises(self, monkeypatch):
        monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
        with pytest.raises(ValueError, match="MISTRAL_API_KEY is not set"):
            await MistralClient.call("mistral/mistral-large", "hi")


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

class TestResponseParsing:
    async def test_anthropic_returns_text(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        resp = mock_response({"content": [{"text": "Hello!"}]})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            result = await AnthropicClient.call("anthropic/claude-opus-4-5", "hi")
        assert result == "Hello!"

    async def test_anthropic_bad_format_raises(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        resp = mock_response({"unexpected": "format"})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            with pytest.raises(ValueError, match="Unexpected Anthropic response format"):
                await AnthropicClient.call("anthropic/claude-opus-4-5", "hi")

    async def test_openai_returns_content(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        resp = mock_response({"choices": [{"message": {"content": "Hello!"}}]})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            result = await OpenAIClient.call("openai/gpt-4o", "hi")
        assert result == "Hello!"

    async def test_openai_bad_format_raises(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        resp = mock_response({"unexpected": "format"})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            with pytest.raises(ValueError, match="Unexpected OpenAI response format"):
                await OpenAIClient.call("openai/gpt-4o", "hi")

    async def test_google_returns_text(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
        resp = mock_response({"candidates": [{"content": {"parts": [{"text": "Hello!"}]}}]})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            result = await GoogleClient.call("google/gemini-2.0-flash", "hi")
        assert result == "Hello!"

    async def test_google_bad_format_raises(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
        resp = mock_response({"unexpected": "format"})
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=resp):
            with pytest.raises(ValueError, match="Unexpected Google response format"):
                await GoogleClient.call("google/gemini-2.0-flash", "hi")
