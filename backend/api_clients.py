import os
import httpx
from backend.config import MAX_TOKENS, TEMPERATURE

class APIClient:
    @staticmethod
    async def call_model(model: str, prompt: str, system: str = "") -> str:
        if model.startswith("anthropic/"):
            return await AnthropicClient.call(model, prompt, system)
        elif model.startswith("openai/"):
            return await OpenAIClient.call(model, prompt, system)
        elif model.startswith("google/"):
            return await GoogleClient.call(model, prompt, system)
        elif model.startswith("xai/"):
            return await XAIClient.call(model, prompt, system)
        elif model.startswith("meta/"):
            return await MetaClient.call(model, prompt, system)
        elif model.startswith("mistral/"):
            return await MistralClient.call(model, prompt, system)
        else:
            raise ValueError(f"Unknown model provider: {model}")

class AnthropicClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("anthropic/", "")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": model_name,
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                    "system": system,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]

class OpenAIClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("openai/", "")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        # o-series models use max_completion_tokens and don't support custom temperature
        is_o_series = model_name.startswith("o1") or model_name.startswith("o3") or model_name.startswith("o4")
        payload = {
            "model": model_name,
            "messages": messages,
        }
        if is_o_series:
            payload["max_completion_tokens"] = MAX_TOKENS
        else:
            payload["max_tokens"] = MAX_TOKENS
            payload["temperature"] = TEMPERATURE
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

class GoogleClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("google/", "")
        api_key = os.getenv("GOOGLE_API_KEY")
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
            },
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

class XAIClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("xai/", "")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

class MetaClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("meta/", "meta-llama/")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.together.xyz/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

class MistralClient:
    @staticmethod
    async def call(model: str, prompt: str, system: str = "") -> str:
        model_name = model.replace("mistral/", "")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
