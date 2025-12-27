"""
ProspectiveMemoryClient for RecallBricks Autonomous Agent API
Manages future-oriented memory for scheduled tasks and reminders
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class ProspectiveMemoryClient(BaseAutonomousClient):
    """
    Client for managing agent prospective memory.

    Prospective memory enables AI agents to remember to do things in the future,
    including scheduled tasks, reminders, and event-triggered actions.

    Usage:
        >>> from recallbricks.autonomous import ProspectiveMemoryClient
        >>> client = ProspectiveMemoryClient(api_key="rb_dev_xxx")
        >>>
        >>> # Schedule a reminder
        >>> reminder = client.create(
        ...     agent_id="agent_123",
        ...     content="Follow up with user about API integration",
        ...     trigger_type="time",
        ...     trigger_at="2024-12-28T10:00:00Z"
        ... )
        >>>
        >>> # Check pending reminders
        >>> pending = client.get_pending(agent_id="agent_123")
    """

    def create(
        self,
        agent_id: str,
        content: str,
        trigger_type: str = "time",
        trigger_at: Optional[str] = None,
        trigger_condition: Optional[str] = None,
        priority: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a prospective memory (scheduled task/reminder).

        Args:
            agent_id: Unique identifier for the agent
            content: Task or reminder content
            trigger_type: Type of trigger (time, event, condition)
            trigger_at: ISO timestamp for time-based triggers
            trigger_condition: Condition string for condition-based triggers
            priority: Priority level 0.0-1.0 (default: 0.5)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing created prospective memory

        Example:
            >>> # Time-based reminder
            >>> reminder = client.create(
            ...     agent_id="agent_123",
            ...     content="Check on deployment status",
            ...     trigger_type="time",
            ...     trigger_at="2024-12-28T14:00:00Z"
            ... )
            >>>
            >>> # Event-based reminder
            >>> reminder = client.create(
            ...     agent_id="agent_123",
            ...     content="Notify user about completion",
            ...     trigger_type="event",
            ...     trigger_condition="task.status == 'completed'"
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not content:
            raise ValueError("content is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "content": self._sanitize_input(content),
            "trigger_type": trigger_type,
            "priority": max(0.0, min(1.0, priority))
        }

        if trigger_at:
            payload["trigger_at"] = trigger_at
        if trigger_condition:
            payload["trigger_condition"] = trigger_condition
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/prospective-memory", json=payload)

    def get(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a specific prospective memory by ID.

        Args:
            memory_id: ID of the prospective memory

        Returns:
            Dict containing prospective memory details

        Example:
            >>> memory = client.get(memory_id="pm_123")
            >>> print(f"Trigger at: {memory['trigger_at']}")
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        return self._request("GET", f"/api/autonomous/prospective-memory/{memory_id}")

    def get_pending(
        self,
        agent_id: str,
        limit: int = 10,
        include_triggered: bool = False
    ) -> Dict[str, Any]:
        """
        Get pending prospective memories for an agent.

        Args:
            agent_id: Unique identifier for the agent
            limit: Maximum number of memories to retrieve (default: 10)
            include_triggered: Include already triggered memories (default: False)

        Returns:
            Dict containing list of pending memories

        Example:
            >>> pending = client.get_pending(agent_id="agent_123")
            >>> for mem in pending['memories']:
            ...     print(f"{mem['content']} - triggers at {mem['trigger_at']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {
            "agent_id": agent_id,
            "limit": limit,
            "include_triggered": include_triggered
        }

        return self._request("GET", "/api/autonomous/prospective-memory", params=params)

    def check_triggers(self, agent_id: str) -> Dict[str, Any]:
        """
        Check for triggered prospective memories.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing list of triggered memories

        Example:
            >>> triggered = client.check_triggers(agent_id="agent_123")
            >>> for mem in triggered['triggered']:
            ...     print(f"Triggered: {mem['content']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "POST",
            "/api/autonomous/prospective-memory/check",
            json={"agent_id": self._sanitize_input(agent_id, max_length=256)}
        )

    def mark_completed(
        self,
        memory_id: str,
        outcome: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark a prospective memory as completed.

        Args:
            memory_id: ID of the prospective memory
            outcome: Optional outcome description

        Returns:
            Dict containing updated memory

        Example:
            >>> client.mark_completed(
            ...     memory_id="pm_123",
            ...     outcome="User was notified successfully"
            ... )
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        payload = {"status": "completed"}
        if outcome:
            payload["outcome"] = self._sanitize_input(outcome)

        return self._request(
            "PUT",
            f"/api/autonomous/prospective-memory/{memory_id}",
            json=payload
        )

    def cancel(self, memory_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel a pending prospective memory.

        Args:
            memory_id: ID of the prospective memory
            reason: Optional cancellation reason

        Returns:
            Dict containing cancellation confirmation

        Example:
            >>> client.cancel(memory_id="pm_123", reason="No longer needed")
        """
        if not memory_id:
            raise ValueError("memory_id is required")

        payload = {"status": "cancelled"}
        if reason:
            payload["reason"] = self._sanitize_input(reason)

        return self._request(
            "PUT",
            f"/api/autonomous/prospective-memory/{memory_id}",
            json=payload
        )

    def reschedule(
        self,
        memory_id: str,
        trigger_at: str
    ) -> Dict[str, Any]:
        """
        Reschedule a time-based prospective memory.

        Args:
            memory_id: ID of the prospective memory
            trigger_at: New trigger timestamp (ISO format)

        Returns:
            Dict containing updated memory

        Example:
            >>> client.reschedule(
            ...     memory_id="pm_123",
            ...     trigger_at="2024-12-29T10:00:00Z"
            ... )
        """
        if not memory_id:
            raise ValueError("memory_id is required")
        if not trigger_at:
            raise ValueError("trigger_at is required")

        return self._request(
            "PUT",
            f"/api/autonomous/prospective-memory/{memory_id}",
            json={"trigger_at": trigger_at}
        )
