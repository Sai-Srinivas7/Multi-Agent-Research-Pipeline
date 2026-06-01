import argparse
import os
import sys

from crewai import Crew, Process

from agents import researcher, fact_checker, tech_writer
from config import DEFAULT_TOPIC, MAX_RPM, OUTPUT_FILE
from tasks import build_tasks


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a multi-agent research crew that writes a Markdown report on a topic."
    )
    parser.add_argument(
        "-t", "--topic",
        default=DEFAULT_TOPIC,
        help="The topic to research (default: newest AI improvements).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.getenv("GROQ_API_KEY"):
        sys.exit(
            "Error: GROQ_API_KEY is not set.\n"
            "Copy .env.example to .env and add your key (https://console.groq.com/keys)."
        )

    print("=" * 48)
    print("Initializing Deep Dive Research Crew...")
    print(f"Topic: {args.topic}")
    print("=" * 48)

    crew = Crew(
        agents=[researcher, fact_checker, tech_writer],
        tasks=build_tasks(args.topic),
        process=Process.sequential,   # Execute tasks in order
        cache=False,                  # Avoid Groq API errors from cached payloads
        max_rpm=MAX_RPM,              # Throttle to stay under Groq's free-tier rate limit
    )

    print("Starting the research process. This may take a few minutes as the agents search the web...")

    try:
        result = crew.kickoff()
    except Exception as exc:  # noqa: BLE001 -- surface a clean message instead of a traceback
        sys.exit(f"\nThe crew failed to complete: {exc}")

    print("\n" + "=" * 48)
    print("RESEARCH COMPLETE!")
    print("=" * 48)
    print(f"The full report has been saved to '{OUTPUT_FILE}'.")
    print("\nHere is a quick preview of the result:\n")
    print(result)


if __name__ == "__main__":
    main()
