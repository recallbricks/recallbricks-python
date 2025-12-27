"""
MemoryTypesClient for RecallBricks Autonomous Agent API
Manages different types of memory (episodic, semantic, procedural)
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class MemoryTypesClient(BaseAutonomousClient):
    """
    Client for managing different memory types.

    Supports episodic (events), semantic (facts), and procedural (how-to) memories,
    enabling agents to store and retrieve information in cognitively appropriate ways.

    Usage:
        >>> from recallbricks.autonomous import MemoryTypesClient
        >>> client = MemoryTypesClient(api_key="rb_dev_xxx")
        >>>
        >>> # Store episodic memory (event)
        >>> client.store_episodic(
        ...     agent_id="agent_123",
        ...     event="User requested password reset",
        ...     context={"user_id": "user_456", "time": "2024-12-27T10:00:00Z"}
        ... )
        >>>
        >>> # Store semantic memory (fact)
        >>> client.store_semantic(
        ...     agent_id="agent_123",
        ...     fact="Python uses indentation for blocks",
        ...     category="programming"
        ... )
    """

    def store_episodic(
        self,
        agent_id: str,
        event: str,
        context: Optional[Dict[str, Any]] = None,
        importance: float = 0.5,
        emotions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store an episodic memory (event/experience).

        Args:
            agent_id: Unique identifier for the agent
            event: Description of the event/experience
            context: Contextual information about the event
            importance: Importance level 0.0-1.0 (default: 0.5)
            emotions: Associated emotions (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing stored episodic memory

        Example:
            >>> client.store_episodic(
            ...     agent_id="agent_123",
            ...     event="Successfully debugged authentication issue",
            ...     context={"project": "api-server", "duration": "2 hours"},
            ...     importance=0.8,
            ...     emotions=["satisfaction", "relief"]
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not event:
            raise ValueError("event is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "memory_type": "episodic",
            "event": self._sanitize_input(event),
            "importance": max(0.0, min(1.0, importance))
        }

        if context:
            payload["context"] = context
        if emotions:
            payload["emotions"] = emotions
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/memory-types", json=payload)

    def store_semantic(
        self,
        agent_id: str,
        fact: str,
        category: Optional[str] = None,
        confidence: float = 0.8,
        source: Optional[str] = None,
        related_concepts: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a semantic memory (fact/knowledge).

        Args:
            agent_id: Unique identifier for the agent
            fact: The fact or knowledge to store
            category: Category for the fact (optional)
            confidence: Confidence in the fact 0.0-1.0 (default: 0.8)
            source: Source of the information (optional)
            related_concepts: Related concepts (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing stored semantic memory

        Example:
            >>> client.store_semantic(
            ...     agent_id="agent_123",
            ...     fact="JWT tokens should be stored in httpOnly cookies",
            ...     category="security",
            ...     confidence=0.95,
            ...     source="OWASP guidelines"
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not fact:
            raise ValueError("fact is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "memory_type": "semantic",
            "fact": self._sanitize_input(fact),
            "confidence": max(0.0, min(1.0, confidence))
        }

        if category:
            payload["category"] = category
        if source:
            payload["source"] = source
        if related_concepts:
            payload["related_concepts"] = related_concepts
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/memory-types", json=payload)

    def store_procedural(
        self,
        agent_id: str,
        skill: str,
        steps: List[str],
        proficiency: float = 0.5,
        prerequisites: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a procedural memory (skill/how-to).

        Args:
            agent_id: Unique identifier for the agent
            skill: Name of the skill/procedure
            steps: Ordered list of steps
            proficiency: Proficiency level 0.0-1.0 (default: 0.5)
            prerequisites: Required prerequisites (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing stored procedural memory

        Example:
            >>> client.store_procedural(
            ...     agent_id="agent_123",
            ...     skill="Deploy to production",
            ...     steps=[
            ...         "Run test suite",
            ...         "Build Docker image",
            ...         "Push to registry",
            ...         "Update Kubernetes deployment"
            ...     ],
            ...     proficiency=0.9,
            ...     prerequisites=["Git access", "K8s credentials"]
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not skill:
            raise ValueError("skill is required")
        if not steps:
            raise ValueError("steps is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "memory_type": "procedural",
            "skill": self._sanitize_input(skill),
            "steps": steps,
            "proficiency": max(0.0, min(1.0, proficiency))
        }

        if prerequisites:
            payload["prerequisites"] = prerequisites
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/memory-types", json=payload)

    def retrieve(
        self,
        agent_id: str,
        memory_type: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve memories by type.

        Args:
            agent_id: Unique identifier for the agent
            memory_type: Filter by type (episodic, semantic, procedural)
            query: Search query (optional)
            limit: Maximum number of results (default: 10)

        Returns:
            Dict containing list of memories

        Example:
            >>> memories = client.retrieve(
            ...     agent_id="agent_123",
            ...     memory_type="semantic",
            ...     query="authentication"
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {"agent_id": agent_id, "limit": limit}
        if memory_type:
            params["memory_type"] = memory_type
        if query:
            params["query"] = query

        return self._request("GET", "/api/autonomous/memory-types", params=params)

    def get_statistics(self, agent_id: str) -> Dict[str, Any]:
        """
        Get memory type statistics for an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing counts and statistics by memory type

        Example:
            >>> stats = client.get_statistics(agent_id="agent_123")
            >>> print(f"Episodic: {stats['episodic']['count']}")
            >>> print(f"Semantic: {stats['semantic']['count']}")
            >>> print(f"Procedural: {stats['procedural']['count']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/memory-types/statistics",
            params={"agent_id": agent_id}
        )

    def consolidate_semantic(
        self,
        agent_id: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Consolidate semantic memories to remove duplicates and conflicts.

        Args:
            agent_id: Unique identifier for the agent
            category: Only consolidate this category (optional)

        Returns:
            Dict containing consolidation results

        Example:
            >>> result = client.consolidate_semantic(
            ...     agent_id="agent_123",
            ...     category="security"
            ... )
            >>> print(f"Merged: {result['merged_count']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        payload = {"agent_id": self._sanitize_input(agent_id, max_length=256)}
        if category:
            payload["category"] = category

        return self._request(
            "POST",
            "/api/autonomous/memory-types/consolidate",
            json=payload
        )
