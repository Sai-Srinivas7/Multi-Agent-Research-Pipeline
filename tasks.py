from crewai import Task

from agents import researcher, fact_checker, tech_writer
from config import OUTPUT_FILE


def build_tasks(topic):
    """Build the sequential research -> fact-check -> write task pipeline for a topic."""
    research_task = Task(
        description=(
            f'Search the web to find the 3 most significant examples of {topic}. '
            'Focus on industry impact.'
        ),
        expected_output='A detailed summary of the 3 items, including what they are and who made them.',
        agent=researcher,
    )

    fact_check_task = Task(
        description=(
            'Take the 3 items identified by the researcher. For each one, use the web to '
            'find 2 concrete, real-world use-cases where it is being applied or could be applied.'
        ),
        expected_output='A verified list of the 3 items, each accompanied by 2 concrete real-world use cases.',
        agent=fact_checker,
    )

    writing_task = Task(
        description='''Using the verified data, write a comprehensive Markdown report.
    For each of the 3 items, the report MUST contain:
    1. A clear explanation of what the improvement is.
    2. The primary use-cases and what it can be used for.
    3. A specific learning path (e.g., what libraries to learn, concepts to study) so a user can learn how to use it.

    Make it engaging and format it beautifully with headers and bullet points.''',
        expected_output='A complete, professional Markdown report saved as a file.',
        agent=tech_writer,
        output_file=OUTPUT_FILE,
    )

    return [research_task, fact_check_task, writing_task]
