# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class MobilityCrew():
    """Academic Mobility Planning Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def transcript_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['transcript_analyst'],
            verbose=True
        )

    @agent
    def course_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['course_matcher'],
            verbose=True
        )

    @agent
    def mobility_plan_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['mobility_plan_generator'],
            verbose=True
        )

    @task
    def transcript_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['transcript_analysis_task']
        )

    @task
    def course_matching_task(self) -> Task:
        return Task(
            config=self.tasks_config['course_matching_task']
        )

    @task
    def mobility_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['mobility_plan_task'],
            output_file='mobility_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Academic Mobility Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )