"""
SearchClient for RecallBricks Autonomous Agent API
Provides advanced search capabilities across agent memories
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class SearchClient(BaseAutonomousClient):
    """
    Client for advanced memory search capabilities.

    Provides semantic search, filtered search, and multi-memory-type search
    capabilities for autonomous agents.

    Usage:
        >>> from recallbricks.autonomous import SearchClient
        >>> client = SearchClient(api_key="rb_dev_xxx")
        >>>
        >>> # Semantic search
        >>> results = client.semantic(
        ...     agent_id="agent_123",
        ...     query="authentication best practices"
        ... )
        >>>
        >>> # Search with filters
        >>> results = client.filtered(
        ...     agent_id="agent_123",
        ...     query="security",
        ...     filters={"memory_type": "semantic", "category": "security"}
        ... )
    """

    def semantic(
        self,
        agent_id: str,
        query: str,
        limit: int = 10,
        min_score: float = 0.0,
        memory_types: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform semantic search across agent memories.

        Args:
            agent_id: Unique identifier for the agent
            query: Search query
            limit: Maximum number of results (default: 10)
            min_score: Minimum relevance score (default: 0.0)
            memory_types: Filter by memory types (optional)
            metadata: Additional search metadata (optional)

        Returns:
            Dict containing search results with relevance scores

        Example:
            >>> results = client.semantic(
            ...     agent_id="agent_123",
            ...     query="API authentication patterns",
            ...     limit=5,
            ...     min_score=0.7
            ... )
            >>> for result in results['results']:
            ...     print(f"{result['content']} (score: {result['score']})")
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not query:
            raise ValueError("query is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "query": self._sanitize_input(query),
            "limit": limit,
            "min_score": min_score
        }

        if memory_types:
            payload["memory_types"] = memory_types
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/search", json=payload)

    def filtered(
        self,
        agent_id: str,
        query: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        sort_by: str = "relevance"
    ) -> Dict[str, Any]:
        """
        Search with filters and optional query.

        Args:
            agent_id: Unique identifier for the agent
            query: Optional search query
            filters: Filter criteria (optional)
            limit: Maximum number of results (default: 10)
            sort_by: Sort order (relevance, created_at, priority)

        Returns:
            Dict containing filtered search results

        Example:
            >>> results = client.filtered(
            ...     agent_id="agent_123",
            ...     query="security",
            ...     filters={
            ...         "memory_type": "semantic",
            ...         "category": "security",
            ...         "created_after": "2024-01-01"
            ...     }
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "limit": limit,
            "sort_by": sort_by
        }

        if query:
            payload["query"] = self._sanitize_input(query)
        if filters:
            payload["filters"] = filters

        return self._request("POST", "/api/autonomous/search/filtered", json=payload)

    def hybrid(
        self,
        agent_id: str,
        query: str,
        keyword_weight: float = 0.3,
        semantic_weight: float = 0.7,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Perform hybrid search combining keyword and semantic search.

        Args:
            agent_id: Unique identifier for the agent
            query: Search query
            keyword_weight: Weight for keyword matching (default: 0.3)
            semantic_weight: Weight for semantic matching (default: 0.7)
            limit: Maximum number of results (default: 10)

        Returns:
            Dict containing hybrid search results

        Example:
            >>> results = client.hybrid(
            ...     agent_id="agent_123",
            ...     query="JWT authentication token",
            ...     keyword_weight=0.4,
            ...     semantic_weight=0.6
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not query:
            raise ValueError("query is required")

        return self._request(
            "POST",
            "/api/autonomous/search/hybrid",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "query": self._sanitize_input(query),
                "keyword_weight": keyword_weight,
                "semantic_weight": semantic_weight,
                "limit": limit
            }
        )

    def similar(
        self,
        agent_id: str,
        memory_id: str,
        limit: int = 10,
        exclude_self: bool = True
    ) -> Dict[str, Any]:
        """
        Find memories similar to a specific memory.

        Args:
            agent_id: Unique identifier for the agent
            memory_id: ID of the reference memory
            limit: Maximum number of results (default: 10)
            exclude_self: Exclude the reference memory (default: True)

        Returns:
            Dict containing similar memories

        Example:
            >>> similar = client.similar(
            ...     agent_id="agent_123",
            ...     memory_id="mem_456",
            ...     limit=5
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not memory_id:
            raise ValueError("memory_id is required")

        return self._request(
            "POST",
            "/api/autonomous/search/similar",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "memory_id": memory_id,
                "limit": limit,
                "exclude_self": exclude_self
            }
        )

    def temporal(
        self,
        agent_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search memories within a time range.

        Args:
            agent_id: Unique identifier for the agent
            start_time: Start of time range (ISO format)
            end_time: End of time range (ISO format)
            query: Optional query within time range
            limit: Maximum number of results (default: 20)

        Returns:
            Dict containing temporal search results

        Example:
            >>> results = client.temporal(
            ...     agent_id="agent_123",
            ...     start_time="2024-12-01T00:00:00Z",
            ...     end_time="2024-12-27T23:59:59Z",
            ...     query="authentication"
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "limit": limit
        }

        if start_time:
            payload["start_time"] = start_time
        if end_time:
            payload["end_time"] = end_time
        if query:
            payload["query"] = self._sanitize_input(query)

        return self._request("POST", "/api/autonomous/search/temporal", json=payload)

    def aggregate(
        self,
        agent_id: str,
        group_by: str,
        query: Optional[str] = None,
        aggregation: str = "count"
    ) -> Dict[str, Any]:
        """
        Aggregate memories by a field.

        Args:
            agent_id: Unique identifier for the agent
            group_by: Field to group by (category, memory_type, etc.)
            query: Optional query to filter before aggregation
            aggregation: Aggregation type (count, avg_score, etc.)

        Returns:
            Dict containing aggregation results

        Example:
            >>> agg = client.aggregate(
            ...     agent_id="agent_123",
            ...     group_by="category",
            ...     aggregation="count"
            ... )
            >>> for bucket in agg['buckets']:
            ...     print(f"{bucket['key']}: {bucket['count']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not group_by:
            raise ValueError("group_by is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "group_by": group_by,
            "aggregation": aggregation
        }

        if query:
            payload["query"] = self._sanitize_input(query)

        return self._request("POST", "/api/autonomous/search/aggregate", json=payload)

    def suggest(
        self,
        agent_id: str,
        partial_query: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get search suggestions based on partial query.

        Args:
            agent_id: Unique identifier for the agent
            partial_query: Partial search query
            limit: Maximum number of suggestions (default: 5)

        Returns:
            Dict containing search suggestions

        Example:
            >>> suggestions = client.suggest(
            ...     agent_id="agent_123",
            ...     partial_query="auth"
            ... )
            >>> # Returns: ["authentication", "authorization", "auth tokens"]
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not partial_query:
            raise ValueError("partial_query is required")

        return self._request(
            "POST",
            "/api/autonomous/search/suggest",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "partial_query": self._sanitize_input(partial_query),
                "limit": limit
            }
        )
