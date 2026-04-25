# Zaya — Local Voice AI Assistant

A fully local, privacy-first voice AI assistant built by **Rambabu Arabandi**.
No cloud APIs, no API keys — everything runs on your own machine.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TailwindCSS |
| Voice UI | LiveKit Components (WebRTC) |
| LLM | Ollama — llama3.2 (local) |
| STT | speaches — Whisper (local) |
| TTS | kokoro-fastapi — Kokoro (local) |
| WebRTC | LiveKit Server (self-hosted via Docker) |

## Project Structure

```
Zaya-new-Voice/
├── app/                  - Next.js app router
│   └── api/token/        - LiveKit token API (dev only)
├── backend/              - Python AI agent
│   └── src/agent.py      - Voice pipeline (STT → LLM → TTS)
├── components/
│   ├── agents-ui/        - Voice UI components
│   ├── app/              - App shell & view controller
│   └── ui/               - Base UI primitives
├── hooks/                - React hooks
├── lib/                  - Utilities & config
└── app-config.ts         - App branding & feature flags
```

## Running Locally

Start all 6 services in separate terminals:

**1. LiveKit Server (WebRTC)**
```bash
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server --dev
```

**2. Ollama (LLM)**
```bash
ollama serve
# make sure llama3.2 is pulled: ollama pull llama3.2
```

**3. speaches (STT — local Whisper)**
```bash
pip install speaches && speaches
```

**4. kokoro-fastapi (TTS — local Kokoro)**
```bash
docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2
```

**5. Python Agent (backend)**
```bash
cd backend
uv run python src/agent.py download-files
uv run python src/agent.py dev
```

**6. Frontend**
```bash
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) and click **Start call**.

## Environment Variables

Create `.env.local` in the root and in `backend/`:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

## License

MIT — Copyright (c) 2025 Rambabu Arabandi
