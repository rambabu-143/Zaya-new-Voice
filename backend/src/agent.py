import logging

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    room_io,
)
from livekit.plugins import openai as lk_openai
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# All three services run locally — no API keys needed
OLLAMA_BASE_URL = "http://localhost:11434/v1"       # ollama serve
SPEACHES_BASE_URL = "http://localhost:8000/v1"      # speaches (local Whisper)
KOKORO_BASE_URL = "http://localhost:8880/v1"        # kokoro-fastapi (local TTS)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant. The user is interacting with you via voice.
            Keep your responses concise and conversational, without formatting, emojis, or symbols.""",
        )


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        # STT: local Whisper via speaches (http://localhost:8000)
        stt=lk_openai.STT(
            base_url=SPEACHES_BASE_URL,
            api_key="speaches",
            model="Systran/faster-whisper-base.en",
        ),
        # LLM: local Ollama (http://localhost:11434)
        llm=lk_openai.LLM(
            base_url=OLLAMA_BASE_URL,
            api_key="ollama",
            model="llama3.2",
        ),
        # TTS: local Kokoro via kokoro-fastapi (http://localhost:8880)
        tts=lk_openai.TTS(
            base_url=KOKORO_BASE_URL,
            api_key="kokoro",
            model="kokoro",
            voice="af_heart",
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    await session.start(agent=Assistant(), room=ctx.room)
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
