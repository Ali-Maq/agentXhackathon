"""
Base executor for Green Agents (evaluators).
"""

from typing import Dict, Any, List, Optional, AsyncIterator
from abc import ABC, abstractmethod
import asyncio
from .models import (
    AssessmentRequest,
    AssessmentResult,
    TaskUpdate,
    Artifact,
    AgentCard
)
from .client import A2AClient, A2AServer


class GreenAgentExecutor(A2AServer, ABC):
    """
    Base class for Green Agent (evaluator) implementation.

    A green agent:
    1. Receives an assessment_request with participants and config
    2. Orchestrates the assessment by communicating with purple agents
    3. Evaluates performance and produces results
    4. Returns artifacts with assessment outcomes
    """

    def __init__(self, name: str, url: str, description: str = ""):
        super().__init__(name, url, description)
        self.client = A2AClient()

    @abstractmethod
    async def setup_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> None:
        """
        Set up the assessment environment.

        Args:
            task_id: Unique identifier for this assessment
            participants: Map of role -> agent_url
            config: Assessment configuration
        """
        pass

    @abstractmethod
    async def run_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> AsyncIterator[TaskUpdate]:
        """
        Execute the assessment and yield progress updates.

        Args:
            task_id: Unique identifier for this assessment
            participants: Map of role -> agent_url
            config: Assessment configuration

        Yields:
            TaskUpdate: Progress updates during assessment
        """
        pass

    @abstractmethod
    async def evaluate_results(
        self,
        task_id: str,
        collected_data: Any
    ) -> AssessmentResult:
        """
        Evaluate the assessment and produce final results.

        Args:
            task_id: Unique identifier for this assessment
            collected_data: Data collected during assessment

        Returns:
            AssessmentResult: Final assessment outcome with score and artifacts
        """
        pass

    async def handle_assessment_request(
        self,
        request: AssessmentRequest
    ) -> AsyncIterator[TaskUpdate | AssessmentResult]:
        """
        Main entry point for assessment requests.
        Orchestrates the full assessment lifecycle.
        """
        task_id = request.task_id
        participants = request.participants
        config = request.config

        try:
            # Setup phase
            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Setting up assessment environment",
                progress=0.1
            )
            await self.setup_assessment(task_id, participants, config)

            # Run phase
            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Running assessment",
                progress=0.2
            )

            collected_data = []
            async for update in self.run_assessment(task_id, participants, config):
                collected_data.append(update)
                yield update

            # Evaluation phase
            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Evaluating results",
                progress=0.9
            )
            result = await self.evaluate_results(task_id, collected_data)

            # Store artifacts
            for artifact in result.artifacts:
                self.store_artifact(task_id, artifact)

            yield result

        except Exception as e:
            yield AssessmentResult(
                task_id=task_id,
                status="failed",
                details={"error": str(e)}
            )

    async def handle_task(self, task_id: str, payload: Dict[str, Any]) -> Any:
        """Handle incoming A2A task messages."""
        if payload.get("type") == "assessment_request":
            request = AssessmentRequest(
                task_id=task_id,
                participants=payload.get("participants", {}),
                config=payload.get("config", {}),
                metadata=payload.get("metadata", {})
            )

            results = []
            async for item in self.handle_assessment_request(request):
                results.append(item)

            return results[-1] if results else None

        return {"error": "Unknown task type"}

    async def get_participant_card(self, agent_url: str) -> AgentCard:
        """Fetch a participant's agent card."""
        return await self.client.get_agent_card(agent_url)

    async def send_to_participant(
        self,
        agent_url: str,
        task_id: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a message to a participant agent."""
        return await self.client.send_task(
            agent_url=agent_url,
            task_id=task_id,
            payload=payload,
            sender=self.url
        )

    async def close(self):
        """Clean up resources."""
        await self.client.close()
