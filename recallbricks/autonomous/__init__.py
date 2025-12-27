"""
RecallBricks Autonomous Agent SDK
Cognitive capabilities for autonomous AI agents

This module provides specialized clients for managing different aspects
of autonomous agent memory and cognition:

- WorkingMemoryClient: Active, short-term memory management
- ProspectiveMemoryClient: Future-oriented memory (reminders, scheduled tasks)
- MetacognitionClient: Self-awareness and reasoning about cognition
- MemoryTypesClient: Episodic, semantic, and procedural memory
- GoalsClient: Goal setting and progress tracking
- HealthClient: Agent health and performance monitoring
- UncertaintyClient: Confidence calibration and uncertainty tracking
- ContextClient: Session and environmental context management
- SearchClient: Advanced memory search capabilities

Usage:
    >>> from recallbricks.autonomous import WorkingMemoryClient, GoalsClient
    >>>
    >>> # Initialize clients
    >>> working_memory = WorkingMemoryClient(api_key="rb_dev_xxx")
    >>> goals = GoalsClient(api_key="rb_dev_xxx")
    >>>
    >>> # Use working memory
    >>> working_memory.store(
    ...     agent_id="agent_123",
    ...     content="User is asking about authentication"
    ... )
    >>>
    >>> # Create a goal
    >>> goals.create(
    ...     agent_id="agent_123",
    ...     title="Implement OAuth integration"
    ... )
"""

from .base import BaseAutonomousClient
from .working_memory import WorkingMemoryClient
from .prospective_memory import ProspectiveMemoryClient
from .metacognition import MetacognitionClient
from .memory_types import MemoryTypesClient
from .goals import GoalsClient
from .health import HealthClient
from .uncertainty import UncertaintyClient
from .context import ContextClient
from .search import SearchClient

__all__ = [
    # Base class
    "BaseAutonomousClient",
    # Client classes
    "WorkingMemoryClient",
    "ProspectiveMemoryClient",
    "MetacognitionClient",
    "MemoryTypesClient",
    "GoalsClient",
    "HealthClient",
    "UncertaintyClient",
    "ContextClient",
    "SearchClient",
]
