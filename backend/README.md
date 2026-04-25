# Zaya — Python Voice Agent (Backend)

The AI backend for Zaya, built by **Rambabu Arabandi**.
Runs a fully local voice pipeline — no cloud APIs, no API keys.

## Pipeline

```
User mic → speaches (Whisper STT) → Ollama (llama3.2 LLM) → kokoro-fastapi (Kokoro TTS) → Speaker
```

## Local Services Required

| Service | Port | How to run |
|---|---|---|
| Ollama (LLM) | 11434 | `ollama serve` |
| speaches (STT) | 8000 | `pip install speaches && speaches` |
| kokoro-fastapi (TTS) | 8880 | `docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2` |
| LiveKit Server | 7880 | `docker run ... livekit/livekit-server --dev` |

## Setup

```bash
# Install dependencies
uv sync

# Download VAD + turn detector models
uv run python src/agent.py download-files

# Run the agent
uv run python src/agent.py dev
```

## Environment Variables

Create `backend/.env.local`:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

## License

MIT — Copyright (c) 2025 Rambabu Arabandi
