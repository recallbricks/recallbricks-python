"""
RecallBricks Python SDK
The Memory Layer for AI

Usage with API key (user-level access):
    >>> from recallbricks import RecallBricks
    >>> memory = RecallBricks(api_key="rb_dev_xxx")
    >>> memory.save("Important information to remember")
    >>> memories = memory.get_all()

Usage with service token (server-to-server access):
    >>> from recallbricks import RecallBricks
    >>> memory = RecallBricks(service_token="rbk_service_xxx")
    >>> memory.save("Important information to remember")
    >>> memories = memory.get_all()

Autonomous Agent Features (v1.3.0+):
    >>> from recallbricks.autonomous import (
    ...     WorkingMemoryClient,
    ...     GoalsClient,
    ...     MetacognitionClient
    ... )
    >>> working_memory = WorkingMemoryClient(api_key="rb_dev_xxx")
    >>> working_memory.store(agent_id="agent_123", content="Context info")
"""

from .client import RecallBricks
from .autonomous import (
    WorkingMemoryClient,
    ProspectiveMemoryClient,
    MetacognitionClient,
    MemoryTypesClient,
    GoalsClient,
    HealthClient,
    UncertaintyClient,
    ContextClient,
    SearchClient,
)
from .exceptions import (
    RecallBricksError,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError,
    NotFoundError
)
from .types import (
    PredictedMemory,
    SuggestedMemory,
    LearningMetrics,
    LearningTrends,
    PatternAnalysis,
    WeightedSearchResult,
    # Phase 2B: Automatic Metatags types
    MemoryMetadata,
    CategorySummary,
    RecallMemory,
    RecallResponse,
    LearnedMemory,
    OrganizedRecallResult
)

__version__ = "1.3.0"
__all__ = [
    "RecallBricks",
    # Autonomous Agent Clients
    "WorkingMemoryClient",
    "ProspectiveMemoryClient",
    "MetacognitionClient",
    "MemoryTypesClient",
    "GoalsClient",
    "HealthClient",
    "UncertaintyClient",
    "ContextClient",
    "SearchClient",
    # Exceptions
    "RecallBricksError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "ValidationError",
    "NotFoundError",
    # Phase 2A types
    "PredictedMemory",
    "SuggestedMemory",
    "LearningMetrics",
    "LearningTrends",
    "PatternAnalysis",
    "WeightedSearchResult",
    # Phase 2B types
    "MemoryMetadata",
    "CategorySummary",
    "RecallMemory",
    "RecallResponse",
    "LearnedMemory",
    "OrganizedRecallResult"
]
