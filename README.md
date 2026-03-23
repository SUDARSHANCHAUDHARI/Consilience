# 🧠 Consilience

> *"The unity of knowledge"* — a multi-AI debate system where multiple AI models collaborate to answer your questions.

Instead of asking one AI, Consilience orchestrates a structured debate between models from Anthropic, OpenAI, Google, xAI, Meta, and Mistral. They respond independently, review each other anonymously, and a Chairman model synthesizes the best insights into one final answer.

Inspired by [Andrej Karpathy's LLM Council](https://x.com/karpathy) concept.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Set up the backend](#2-set-up-the-backend)
  - [3. Set up the frontend](#3-set-up-the-frontend)
  - [4. Configure API keys](#4-configure-api-keys)
- [Running the App](#running-the-app)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Free Setup (No Cost)](#free-setup-no-cost)
- [Getting API Keys](#getting-api-keys)
- [Configuration](#configuration)
  - [Changing which models are used](#changing-which-models-are-used)
  - [Changing the Chairman](#changing-the-chairman)
  - [Adjusting response settings](#adjusting-response-settings)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Cost Guide](#cost-guide)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## How It Works

Every query goes through 3 stages:

```
Your Question
     │
     ▼
┌─────────────────────────────────────────┐
│  Stage 1: Individual Responses          │
│  All models answer independently        │
│  (runs in parallel)                     │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Stage 2: Peer Reviews                  │
│  Each model reviews the others          │
│  (responses are anonymized)             │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Stage 3: Chairman's Final Answer       │
│  One model reads everything and         │
│  synthesizes the best final answer      │
└─────────────────────────────────────────┘
     │
     ▼
  Result displayed in UI
  Conversation saved to JSON
```

**Why anonymized reviews?**
In Stage 2, model names are hidden (replaced with "Response 1", "Response 2", etc.) so models can't favour themselves or be biased toward well-known competitors.

**Total API calls per query:** 21 (10 responses + 10 reviews + 1 synthesis)

---

## Requirements

### System
- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **pnpm** (Node package manager)

### Check your versions

```bash
python3 --version    # should be 3.10+
node --version       # should be 18+
pnpm --version       # should be installed
```

### Install pnpm (if not installed)

```bash
npm install -g pnpm
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Consilience
```

### 2. Set up the backend

Create a Python virtual environment and install dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate          # macOS / Linux
# OR
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
```

You should see output confirming packages like `fastapi`, `uvicorn`, `httpx`, `pydantic` are installed.

### 3. Set up the frontend

```bash
cd frontend
pnpm install
cd ..
```

### 4. Configure API keys

Copy the example env file:

```bash
cp .env.example .env
```

Open `.env` in a text editor and fill in your API keys:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-key-here
XAI_API_KEY=xai-your-key-here
TOGETHER_API_KEY=your-key-here
MISTRAL_API_KEY=your-key-here
```

> You do **not** need all keys. See [Free Setup](#free-setup-no-cost) to start with just free providers.

---

## Running the App

You need two terminals open at the same time.

**Terminal 1 — Start the backend:**

```bash
# Make sure you're in the Consilience/ root directory
source venv/bin/activate          # macOS / Linux
# OR
venv\Scripts\activate             # Windows

python -m backend.main
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 — Start the frontend:**

```bash
cd frontend
pnpm dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

**Open your browser and go to: [http://localhost:5173](http://localhost:5173)**

Type a question, click **Ask Council**, and wait for the 3-stage debate to complete (can take 30–90 seconds depending on how many models are active).

---

## Docker Deployment

The easiest way to run Consilience in production.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed
- A `.env` file with your API keys (copy from `.env.example`)

### Run with Docker Compose

```bash
docker compose up --build
```

This starts:
- **Backend** on port `8000`
- **Frontend** on port `80` (served by nginx)

Open [http://localhost](http://localhost) in your browser.

### Stopping

```bash
docker compose down
```

### Production deployment

To deploy on a server, set the `CORS_ORIGINS` variable in your `.env` to your actual domain:

```env
CORS_ORIGINS=https://yourdomain.com
```

And pass your domain as a build arg for the frontend so the API URL is baked in:

```bash
docker compose build --build-arg VITE_API_URL=https://api.yourdomain.com
docker compose up
```

### Conversation history

Conversations are saved to `data/conversations/` on your host machine via the Docker volume mount in `docker-compose.yml`. They persist across container restarts.

---

## Testing

### Backend tests

Install dev dependencies (one time):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Run all 24 tests:

```bash
python3 -m pytest
```

Run with verbose output:

```bash
python3 -m pytest -v
```

Tests cover:
- **API client routing** — each model prefix routes to the correct provider
- **API key validation** — missing keys raise clear errors for all 6 providers
- **Response parsing** — valid responses return text; malformed responses raise descriptive errors
- **Query endpoint** — health check, missing body, full council response, graceful model error handling

### Frontend tests

```bash
cd frontend
pnpm test
```

Run in watch mode (re-runs on file save):

```bash
pnpm test:watch
```

Tests cover:
- Renders header and form elements
- Ignores empty query submissions
- Disables input/button while loading
- Displays error banner on network failure or server error
- Clears previous error on new submission
- Renders Stage 1 model tabs after successful query
- Renders Stage 3 final answer
- Toggles peer reviews show/hide

---

## Free Setup (No Cost)

You can run Consilience completely free using providers that offer free tiers.

### Which providers are free?

| Provider | Free Tier | Sign up |
|----------|-----------|---------|
| **Google Gemini** | ✅ Free with rate limits | [ai.google.dev](https://ai.google.dev) |
| **Together AI** (Llama) | ✅ $1 free credit on signup | [api.together.xyz](https://api.together.xyz) |
| **Mistral** | ✅ Free tier with rate limits | [console.mistral.ai](https://console.mistral.ai) |
| **Anthropic** | ❌ Paid only | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | ❌ Paid only | [platform.openai.com](https://platform.openai.com) |
| **xAI (Grok)** | ❌ Paid only | [x.ai/api](https://x.ai/api) |

### Free config

Edit `backend/config.py` to use only free models:

```python
COUNCIL_MODELS = [
    "google/gemini-2.0-flash",
    "google/gemini-1.5-pro",
    "meta/llama-3.1-70b-instruct",
    "mistral/mistral-large",
]

CHAIRMAN_MODEL = "google/gemini-2.0-flash"
```

In `.env`, only these three keys are needed:

```env
GOOGLE_API_KEY=your-key-here
TOGETHER_API_KEY=your-key-here
MISTRAL_API_KEY=your-key-here
```

This gives you a 4-model council at effectively **$0 per query**.

---

## Getting API Keys

Here is exactly where to get each key:

### Anthropic (Claude)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account and add a payment method
3. Go to **API Keys** → **Create Key**
4. Copy the key starting with `sk-ant-`

### OpenAI (GPT-4o, o1)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account and add a payment method
3. Go to **API Keys** → **Create new secret key**
4. Copy the key starting with `sk-`

### Google (Gemini)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key

### xAI (Grok)
1. Go to [x.ai/api](https://x.ai/api)
2. Sign in with your X (Twitter) account
3. Go to **API** section and create a key
4. Copy the key starting with `xai-`

### Together AI (Llama)
1. Go to [api.together.xyz](https://api.together.xyz)
2. Create a free account (get $1 free credit)
3. Go to **Settings** → **API Keys** → **Create**
4. Copy the key

### Mistral
1. Go to [console.mistral.ai](https://console.mistral.ai)
2. Create a free account
3. Go to **API Keys** → **Create new key**
4. Copy the key

---

## Configuration

All configuration is in `backend/config.py`.

### Changing which models are used

Edit the `COUNCIL_MODELS` list. You can add, remove, or reorder models:

```python
COUNCIL_MODELS = [
    "anthropic/claude-opus-4-5",       # Best quality, most expensive
    "anthropic/claude-sonnet-4-5",     # Balanced quality/cost
    "anthropic/claude-haiku-4-5",      # Fast and cheap
    "openai/gpt-4o",                   # Strong all-rounder
    "openai/o1",                       # Best at reasoning/math
    "google/gemini-2.0-flash",         # Fast, free tier
    "google/gemini-1.5-pro",           # Balanced, free tier
    "xai/grok-beta",                   # Unique perspective
    "meta/llama-3.1-70b-instruct",     # Open source model
    "mistral/mistral-large",           # European AI, free tier
]
```

**Supported model ID format:**

| Provider prefix | Example |
|----------------|---------|
| `anthropic/` | `anthropic/claude-haiku-4-5` |
| `openai/` | `openai/gpt-4o` |
| `google/` | `google/gemini-2.0-flash` |
| `xai/` | `xai/grok-beta` |
| `meta/` | `meta/llama-3.1-70b-instruct` |
| `mistral/` | `mistral/mistral-large` |

> If you only have keys for some providers, **remove the models for providers you don't have keys for**. Models without a valid API key will return errors.

### Changing the Chairman

The Chairman is the model that writes the final synthesized answer. It sees everything — all responses and all reviews — so choose your most capable available model:

```python
CHAIRMAN_MODEL = "anthropic/claude-opus-4-5"   # default
# or
CHAIRMAN_MODEL = "openai/gpt-4o"
# or
CHAIRMAN_MODEL = "google/gemini-2.0-flash"      # free option
```

### Adjusting response settings

```python
MAX_TOKENS = 2000    # Maximum length of each model's response
                     # Lower = faster + cheaper, Higher = more detail

TEMPERATURE = 0.7    # Creativity level: 0.0 = focused/deterministic
                     #                   1.0 = creative/varied
```

---

## Project Structure

```
Consilience/
│
├── backend/                    # Python FastAPI backend
│   ├── __init__.py             # Loads .env on startup
│   ├── config.py               # All settings: models, tokens, temperature
│   ├── api_clients.py          # API call logic for each provider
│   ├── main.py                 # Server, endpoints, 3-stage debate logic
│   └── tests/                  # Backend test suite (pytest)
│       ├── test_api_clients.py # Tests for routing, key validation, response parsing
│       └── test_main.py        # Tests for FastAPI endpoints
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── __tests__/
│   │   │   └── App.test.jsx    # Frontend test suite (Vitest)
│   │   ├── App.jsx             # Main UI — all components and state
│   │   ├── App.css             # All styles (purple gradient theme)
│   │   ├── main.jsx            # React entry point
│   │   └── test-setup.js       # Vitest setup (jest-dom matchers)
│   ├── index.html              # HTML shell
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite + Vitest config
│   ├── Dockerfile              # Frontend Docker image (nginx)
│   └── nginx.conf              # nginx config for SPA routing
│
├── data/
│   └── conversations/          # Auto-saved query history (JSON files)
│
├── venv/                       # Python virtual environment (auto-generated)
├── .env                        # Your API keys (never commit this)
├── .env.example                # Template showing required keys
├── .gitignore                  # Ignores venv, .env, node_modules, etc.
├── Dockerfile                  # Backend Docker image
├── docker-compose.yml          # Runs backend + frontend together
├── requirements.txt            # Python runtime dependencies
├── requirements-dev.txt        # Python dev/test dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

### Key file descriptions

**`backend/config.py`**
The single place to configure everything — which models to use, which is chairman, response length, and creativity. Start here when customizing.

**`backend/api_clients.py`**
Contains one class per AI provider (`AnthropicClient`, `OpenAIClient`, `GoogleClient`, etc.). Each handles the specific API format, authentication, and response parsing for that provider. The `APIClient` class routes calls to the right provider based on the model prefix.

**`backend/main.py`**
The FastAPI server. Contains the `/api/query` endpoint which runs the full 3-stage debate, plus helpers `get_initial_responses()`, `get_reviews()`, and `get_final_answer()`. All stages use `asyncio.gather()` to call models in parallel.

**`frontend/src/App.jsx`**
The entire frontend in one component. Manages all state (query, loading, results, active tab, show/hide reviews) and renders the 3-stage UI.

---

## API Reference

The backend exposes two endpoints at `http://localhost:8000`.

---

### `GET /api/health`

Check if the backend is running.

**Response:**
```json
{
  "status": "ok",
  "models": 10
}
```

---

### `POST /api/query`

Run a question through the full 3-stage debate.

**Request body:**
```json
{
  "query": "What is the meaning of life?"
}
```

**Response:**
```json
{
  "query": "What is the meaning of life?",
  "stage1_responses": [
    {
      "model": "anthropic/claude-opus-4-5",
      "model_name": "Claude Opus 4.5",
      "response": "The meaning of life is a profound philosophical question..."
    },
    {
      "model": "openai/gpt-4o",
      "model_name": "GPT-4o",
      "response": "Philosophers have debated this for centuries..."
    }
    // ... one entry per model in COUNCIL_MODELS
  ],
  "stage2_reviews": [
    {
      "model": "anthropic/claude-opus-4-5",
      "model_name": "Claude Opus 4.5",
      "review": "Ranking: Response 3 > Response 1 > Response 2...\nReasoning: Response 3 offered the most nuanced..."
    }
    // ... one review per model
  ],
  "stage3_final": "After reviewing all council responses and their peer evaluations...",
  "timestamp": "2026-03-16T10:30:00.123456"
}
```

**Error response (500):**
```json
{
  "detail": "Error description"
}
```

> Individual model failures do **not** crash the whole request. A failing model returns `"[Error: ...]"` as its response and the debate continues with the other models.

---

## Cost Guide

Each query makes 21 API calls. Cost depends on which models you use.

### Per-model approximate costs (per query)

| Model | Stage 1 | Stage 2 | Total/query |
|-------|---------|---------|-------------|
| Claude Opus 4.5 | ~$0.05 | ~$0.15 | ~$0.20 |
| Claude Sonnet 4.5 | ~$0.01 | ~$0.03 | ~$0.04 |
| Claude Haiku 4.5 | ~$0.001 | ~$0.003 | ~$0.004 |
| GPT-4o | ~$0.01 | ~$0.03 | ~$0.04 |
| OpenAI o1 | ~$0.05 | ~$0.15 | ~$0.20 |
| Gemini 2.0 Flash | free | free | $0.00 |
| Gemini 1.5 Pro | free | free | $0.00 |
| Grok | ~$0.01 | ~$0.03 | ~$0.04 |
| Llama 3.1 70B | ~$0.001 | ~$0.003 | ~$0.004 |
| Mistral Large | free | free | $0.00 |

> Stage 2 is more expensive because each model receives all other responses as input (much longer prompts).

### Total cost scenarios

| Setup | Models used | Approx. cost/query |
|-------|------------|-------------------|
| Full council (all 10) | All | $0.50 – $1.50 |
| Mid-tier only | Sonnet, GPT-4o, Gemini, Llama, Mistral | $0.05 – $0.15 |
| Cheap only | Haiku, Gemini, Llama, Mistral | $0.01 – $0.05 |
| Free only | Gemini x2, Llama, Mistral | $0.00 |

**Tips to reduce cost:**
- Remove Claude Opus and o1 from `COUNCIL_MODELS` (they're the most expensive)
- Lower `MAX_TOKENS` to 500–1000 for shorter responses
- Use fewer models (4–5 is enough to get diverse perspectives)

---

## Troubleshooting

### Backend won't start

**`ModuleNotFoundError`**
```bash
# Make sure the virtual environment is activated
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# Then reinstall
pip install -r requirements.txt
```

**`Must be run as a module`**
```bash
# Run from the Consilience/ root directory, not inside backend/
python -m backend.main     # correct
python backend/main.py     # wrong
```

### Port already in use

```bash
# Kill whatever is using port 8000
lsof -ti:8000 | xargs kill -9    # macOS/Linux

# Or kill port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### API key errors

Check your `.env` file:
- File is named `.env` (not `.env.example` or `.env.txt`)
- No spaces around `=` (correct: `KEY=value`, wrong: `KEY = value`)
- No quotes around values (correct: `KEY=abc123`, wrong: `KEY="abc123"`)
- Key format is correct (Anthropic starts with `sk-ant-`, OpenAI with `sk-`)

### A model keeps returning `[Error: ...]`

This means that specific model's API call failed. Common reasons:
- No API key set for that provider → remove the model from `COUNCIL_MODELS`
- API key is invalid or expired → check the provider's dashboard
- Rate limit hit → wait a minute and try again, or remove the model
- Model name is wrong → check the supported model IDs in [Configuration](#configuration)

### CORS error in browser console

The backend must be running on port `8000` and the frontend on port `5173`. If you changed either port, update:
- Frontend: set `VITE_API_URL=http://localhost:<your-backend-port>` in `frontend/.env.local`
- Backend: set `CORS_ORIGINS=http://localhost:<your-frontend-port>` in your `.env`

### Slow responses

With 10 models, Stage 1 and Stage 2 each take as long as the **slowest** model (since they run in parallel but wait for all to finish). The timeout per model is 60 seconds. To speed things up:
- Remove slow models (o1 and Opus tend to be slower)
- Lower `MAX_TOKENS` so responses are shorter

---

## FAQ

**Q: Do I need all 6 API keys?**
No. You only need keys for the providers whose models are in your `COUNCIL_MODELS` list. If you remove all OpenAI models from the list, you don't need an OpenAI key.

**Q: Can I use just one model?**
Technically yes — set `COUNCIL_MODELS` to one model and set `CHAIRMAN_MODEL` to the same. But you lose the debate aspect. Two or more models is recommended.

**Q: Where are conversations saved?**
In `data/conversations/` as JSON files, named by timestamp (e.g., `conversation_2026-03-16T10-30-00.json`). They include the full query, all responses, all reviews, and the final answer.

**Q: Can I add a model that isn't listed?**
Yes, as long as the provider is already supported. For example, to add `claude-sonnet-4-6`:
1. Add `"anthropic/claude-sonnet-4-6"` to `COUNCIL_MODELS`
2. Add a display name to `MODEL_DISPLAY_NAMES`: `"anthropic/claude-sonnet-4-6": "Claude Sonnet 4.6"`

**Q: Can I add a completely new AI provider?**
Yes, but it requires adding a new client class in `backend/api_clients.py`. Follow the pattern of existing clients (e.g., copy `MistralClient`, update the URL, headers, and response parsing). Then add routing for the new prefix in `APIClient.call_model()`.

**Q: Why is Stage 2 more expensive than Stage 1?**
In Stage 2, each model receives the original question *plus all responses from Stage 1* as input. With 10 models each writing ~500 words, that's roughly 5,000 words of extra context per Stage 2 call.

**Q: What happens if a model fails?**
The query continues without it. The failed model's response shows as `[Error: ...]` in the UI. The remaining models' reviews and the final answer still work normally.

**Q: Is my data sent to multiple AI companies?**
Yes. Your question is sent to every provider in `COUNCIL_MODELS`. In Stage 2, each provider also receives all other models' responses (anonymized). Do not use Consilience with sensitive or private information.
