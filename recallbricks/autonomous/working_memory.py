"""
WorkingMemoryClient for RecallBricks Autonomous Agent API
Manages active, short-term memory for AI agents
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class WorkingMemoryClient(BaseAutonomousClient):
    """
    Client for managing agent working memory.

    Working memory provides active, short-term memory storage for AI agents,
    enabling them to maintain context during conversations and tasks.

    Usage:
        >>> from recallbricks.autonomous import WorkingMemoryClient
        >>> client = WorkingMemoryClient(api_key="rb_dev_xxx")
        >>>
        >>> # Store working memory
        >>> result = client.store(
        ...     agent_id="agent_123",
        ...     content="User is asking about authentication",
        ...     memory_type="context"
        ... )
        >>>
        >>> # Retrieve working memory
        >>> memories = client.retrieve(agent_id="agent_123")
    """

    def store(
        self,
        agent_id: str,
        content: str,
        memory_type: str = "context",
        priority: float = 0.5,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store content in working memory.

        Args:
            agent_id: Unique identifier for the agent
            content: Memory content to store
            memory_type: Type of memory (context, task, observation)
            priority: Priority level 0.0-1.0 (default: 0.5)
            ttl_seconds: Time-to-live in seconds (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing stored memory with id and timestamps

        Example:
            >>> result = client.store(
            ...     agent_id="agent_123",
            ...     content="User prefers dark mode",
            ...     memory_type="preference",
            ...     priority=0.8
            ... )
            >>> print(f"Stored memory: {result['id']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not content:
            raise ValueError("content is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "content": self._sanitize_input(content),
            "memory_type": memory_type,
            "priority": max(0.0, min(1.0, priority))
        }

        if ttl_seconds is not None:
            payload["ttl_seconds"] = ttl_seconds
        if metadata is not None:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/working-memory", json=payload)

    def retrieve(
        self,
        agent_id: str,
        memory_type: Optional[str] = None,
        limit: int = 10,
        min_priority: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Retrieve working memory for an agent.

        Args:
            agent_id: Unique identifier for the agent
            memory_type: Filter by memory type (optional)
            limit: Maximum number of memories to retrieve (default: 10)
            min_priority: Minimum priority threshold (optional)

        Returns:
            Dict containing list of memories and count

        Example:
            >>> memories = client.retrieve(agent_id="agent_123", limit=5)
            >>> for mem in memories['memories']:
            ...     print(f"{mem['content']} (priority: {mem['priority']})")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {
            "agent_id": agent_id,
            "limit": limit
        }

        if memory_type:
            params["memory_type"] = memory_type
        if min_priority is not None:
            params["min_priority"] = min_priority

        return self._request("GET", "/api/autonomous/working-memory", params=params)

    def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        priority: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing working memory entry.

        Args:
            memory_id: ID of the memory to update
            content: New content (optional)
            priority: New priority level (optional)
            metadata: New metadata (optional)

        Returns:
            Dict containing updated memory

        Example:
            >>> result = client.update(
            ...     memory_id="mem_123",
            ...     priority=0.9
            ... )
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        payload = {}
        if content is not None:
            payload["content"] = self._sanitize_input(content)
        if priority is not None:
            payload["priority"] = max(0.0, min(1.0, priority))
        if metadata is not None:
            payload["metadata"] = metadata

        if not payload:
            raise ValueError("At least one field must be provided for update")

        return self._request(
            "PUT",
            f"/api/autonomous/working-memory/{memory_id}",
            json=payload
        )

    def delete(self, memory_id: str) -> Dict[str, Any]:
        """
        Delete a working memory entry.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            Dict containing deletion confirmation

        Example:
            >>> client.delete(memory_id="mem_123")
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        return self._request("DELETE", f"/api/autonomous/working-memory/{memory_id}")

    def clear(self, agent_id: str, memory_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Clear all working memory for an agent.

        Args:
            agent_id: Unique identifier for the agent
            memory_type: Only clear memories of this type (optional)

        Returns:
            Dict containing number of deleted memories

        Example:
            >>> result = client.clear(agent_id="agent_123")
            >>> print(f"Cleared {result['deleted_count']} memories")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {"agent_id": agent_id}
        if memory_type:
            params["memory_type"] = memory_type

        return self._request("DELETE", "/api/autonomous/working-memory", params=params)

    def consolidate(
        self,
        agent_id: str,
        strategy: str = "importance"
    ) -> Dict[str, Any]:
        """
        Consolidate working memory by moving important items to long-term storage.

        Args:
            agent_id: Unique identifier for the agent
            strategy: Consolidation strategy (importance, recency, relevance)

        Returns:
            Dict containing consolidation results

        Example:
            >>> result = client.consolidate(
            ...     agent_id="agent_123",
            ...     strategy="importance"
            ... )
            >>> print(f"Consolidated {result['consolidated_count']} memories")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "strategy": strategy
        }

        return self._request("POST", "/api/autonomous/working-memory/consolidate", json=payload)
