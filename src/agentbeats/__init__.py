"""
AgentBeats SDK - Core components for building Green and Purple agents.

This package provides:
- A2A protocol integration
- Green agent executor base class
- Purple agent helpers
- Client utilities for agent communication
"""

__version__ = "0.1.0"
__author__ = "AgentX Hackathon Team"

from .models import (
    AgentCard,
    TaskUpdate,
    Artifact,
    AssessmentRequest,
    AssessmentResult,
    A2AMessage,
    DebateConfig,
    CodingTaskConfig,
)
from .client import A2AClient, A2AServer
from .green_executor import GreenAgentExecutor
from .run_scenario import ScenarioRunner, run_scenario_file

__all__ = [
    "__version__",
    "__author__",
    "AgentCard",
    "TaskUpdate",
    "Artifact",
    "AssessmentRequest",
    "AssessmentResult",
    "A2AMessage",
    "DebateConfig",
    "CodingTaskConfig",
    "A2AClient",
    "A2AServer",
    "GreenAgentExecutor",
    "ScenarioRunner",
    "run_scenario_file",
]
