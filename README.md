# Deep Dive Research Crew

A multi-agent AI pipeline built with [CrewAI](https://docs.crewai.com/). Three specialized agents collaborate to research a topic on the live web, verify their findings, and produce a polished Markdown report — complete with real-world use cases and a learning path for each finding.

By default it researches the newest AI improvements, but you can point it at any topic from the command line.

## How it works

The crew runs three agents **sequentially**, each handing its output to the next:

```
        ┌─────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
 topic ─▶│   Researcher    │─────▶│   Fact-Checker   │─────▶│    Tech Writer      │─▶ report.md
        │ finds 3 items   │      │ verifies + finds │      │ writes structured   │
        │ via web search  │      │ real use-cases   │      │ Markdown report     │
        └─────────────────┘      └──────────────────┘      └─────────────────────┘
```

| Agent | Role | Tools |
|-------|------|-------|
| Researcher | Finds the 3 most significant items on the topic | DuckDuckGo web search |
| Fact-Checker | Verifies each item and finds 2 concrete use-cases | DuckDuckGo web search |
| Tech Writer | Synthesizes everything into a structured report | — |

The LLM is Groq's free-tier `llama-3.1-8b-instant`, accessed through CrewAI/LiteLLM.

## Project structure

```
.
├── main.py          # Entry point: parses args, builds and runs the crew
├── agents.py        # The three agent definitions
├── tasks.py         # build_tasks(topic) — the task pipeline
├── tools.py         # DuckDuckGo search tool
├── config.py        # Model, output file, and runtime settings (from .env)
├── groq_patch.py    # Compatibility shim so CrewAI works with Groq's strict API
├── test_smoke.py    # Tests that the crew wires up correctly (no API calls)
├── requirements.txt
└── .env.example     # Copy to .env and add your key
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
cp .env.example .env

```

## Usage

```bash
# Research the default topic (newest AI improvements)
python main.py

# Research any topic you like
python main.py --topic "the best open-source vector databases"
```

The final report is written to `final_ai_report.md` and a preview is printed to the console.

## Running the tests

```bash
pytest            # or: python test_smoke.py
```

These tests confirm the agents and task pipeline are configured correctly. They do **not** call the LLM or the network.

## Configuration

Set these in your `.env` to override the defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | **Required.** Your Groq API key. |
| `GROQ_MODEL` | `groq/llama-3.1-8b-instant` | LLM model string. |
| `OUTPUT_FILE` | `final_ai_report.md` | Where the report is saved. |
| `MAX_RPM` | `2` | Requests per minute, to stay under Groq's free-tier limit. |

## Notes

Groq's API rejects the `cache_breakpoint` key that CrewAI injects into messages. `groq_patch.py` strips that key in a thin wrapper around `LLM.call`. The crew also disables CrewAI's internal cache and throttles requests to avoid hitting free-tier rate limits.

## License

MIT
