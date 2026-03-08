#!/usr/bin/env python

import warnings
from datetime import datetime

from latest_ai_development.crew import MobilityCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the Academic Mobility Crew
    """

    transcript = """
Programming Fundamentals - A
Object Oriented Programming - A-
Data Structures - B+
Algorithms - B
Computer Networks - A-
Operating Systems - B+
Database Systems - A
Discrete Mathematics - B+
Computer Architecture - B
Software Engineering - A-
"""

    course_catalog = """
Advanced Algorithms
Distributed Systems
Cloud Computing
Artificial Intelligence
Machine Learning
Computer Security
Mobile Application Development
Big Data Analytics
Internet of Things
Advanced Database Systems
Software Architecture
"""

    inputs = {
        "transcript": transcript,
        "course_catalog": course_catalog,
        "current_year": str(datetime.now().year)
    }

    try:
        MobilityCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()