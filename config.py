"""Central configuration, loaded from environment variables (.env)."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM model string passed to CrewAI/LiteLLM. Override with GROQ_MODEL in .env.
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/llama-3.1-8b-instant")

# Where the final report is written.
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "final_ai_report.md")

# Default research topic if none is passed on the command line.
DEFAULT_TOPIC = (
    "the most significant, newest AI improvements (frameworks, models, "
    "or techniques) released in the last few months"
)

# Requests-per-minute throttle to stay under Groq's free-tier rate limit.
MAX_RPM = int(os.getenv("MAX_RPM", "2"))
