"""
Pydantic models for AgentBeats A2A protocol messages.
"""

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class AgentCard(BaseModel):
    """A2A Agent Card - describes agent capabilities."""
    name: str
    url: str
    description: Optional[str] = None
    version: Optional[str] = "0.1.0"
    capabilities: Optional[List[str]] = []
    roles: Optional[List[str]] = []


class TaskUpdate(BaseModel):
    """A2A Task Update - progress notification."""
    task_id: str
    status: Literal["pending", "in_progress", "completed", "failed"]
    message: Optional[str] = None
    progress: Optional[float] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = {}


class Artifact(BaseModel):
    """A2A Artifact - output from an assessment."""
    name: str
    content: str
    content_type: str = "text/plain"
    metadata: Optional[Dict[str, Any]] = {}


class AssessmentRequest(BaseModel):
    """Request to start an assessment."""
    task_id: str
    participants: Dict[str, str]  # role -> agent_url
    config: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = {}


class AssessmentResult(BaseModel):
    """Result of an assessment."""
    task_id: str
    status: Literal["completed", "failed"]
    score: Optional[float] = None
    details: Optional[Dict[str, Any]] = {}
    artifacts: List[Artifact] = []
    metadata: Optional[Dict[str, Any]] = {}


class A2AMessage(BaseModel):
    """Generic A2A protocol message."""
    message_type: str
    task_id: str
    sender: str
    recipient: str
    payload: Dict[str, Any]
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class DebateConfig(BaseModel):
    """Configuration for debate assessment."""
    topic: str
    rounds: int = 3
    time_limit: Optional[int] = None
    judging_criteria: Optional[List[str]] = ["argument_quality", "coherence", "persuasiveness"]


class CodingTaskConfig(BaseModel):
    """Configuration for coding assessment."""
    task_description: str
    test_cases: List[Dict[str, Any]]
    time_limit: Optional[int] = 300  # seconds
    language: Optional[str] = "python"
    allowed_libraries: Optional[List[str]] = []
