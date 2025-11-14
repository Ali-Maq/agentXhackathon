"""
A2A client utilities for agent communication.
"""

import httpx
import json
from typing import Any, Dict, Optional, AsyncIterator
from .models import AgentCard, A2AMessage, TaskUpdate, Artifact


class A2AClient:
    """Client for A2A protocol communication."""

    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get_agent_card(self, agent_url: str) -> AgentCard:
        """Fetch an agent's card."""
        response = await self.client.get(f"{agent_url}/card")
        response.raise_for_status()
        return AgentCard(**response.json())

    async def send_task(
        self,
        agent_url: str,
        task_id: str,
        payload: Dict[str, Any],
        sender: str = "controller"
    ) -> Dict[str, Any]:
        """Send a task to an agent."""
        message = A2AMessage(
            message_type="task",
            task_id=task_id,
            sender=sender,
            recipient=agent_url,
            payload=payload
        )

        response = await self.client.post(
            f"{agent_url}/task",
            json=message.model_dump(mode="json")
        )
        response.raise_for_status()
        return response.json()

    async def stream_task(
        self,
        agent_url: str,
        task_id: str,
        payload: Dict[str, Any],
        sender: str = "controller"
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream task updates from an agent."""
        message = A2AMessage(
            message_type="task",
            task_id=task_id,
            sender=sender,
            recipient=agent_url,
            payload=payload
        )

        async with self.client.stream(
            "POST",
            f"{agent_url}/task/stream",
            json=message.model_dump(mode="json")
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    async def get_artifact(self, agent_url: str, task_id: str, artifact_name: str) -> Artifact:
        """Retrieve an artifact from an agent."""
        response = await self.client.get(
            f"{agent_url}/task/{task_id}/artifact/{artifact_name}"
        )
        response.raise_for_status()
        return Artifact(**response.json())

    async def close(self):
        """Close the client connection."""
        await self.client.aclose()


class A2AServer:
    """Base class for A2A server implementation."""

    def __init__(self, name: str, url: str, description: str = ""):
        self.name = name
        self.url = url
        self.description = description
        self.tasks: Dict[str, Any] = {}
        self.artifacts: Dict[str, Dict[str, Artifact]] = {}

    def get_card(self) -> AgentCard:
        """Return agent card."""
        return AgentCard(
            name=self.name,
            url=self.url,
            description=self.description
        )

    async def handle_task(self, task_id: str, payload: Dict[str, Any]) -> Any:
        """Override this method to handle incoming tasks."""
        raise NotImplementedError

    def store_artifact(self, task_id: str, artifact: Artifact):
        """Store an artifact for a task."""
        if task_id not in self.artifacts:
            self.artifacts[task_id] = {}
        self.artifacts[task_id][artifact.name] = artifact

    def get_artifact(self, task_id: str, artifact_name: str) -> Optional[Artifact]:
        """Retrieve a stored artifact."""
        return self.artifacts.get(task_id, {}).get(artifact_name)
