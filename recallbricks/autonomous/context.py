"""
ContextClient for RecallBricks Autonomous Agent API
Manages agent context, session state, and environmental awareness
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class ContextClient(BaseAutonomousClient):
    """
    Client for managing agent context and sessions.

    Enables agents to maintain awareness of their current context,
    manage session state, and understand their operational environment.

    Usage:
        >>> from recallbricks.autonomous import ContextClient
        >>> client = ContextClient(api_key="rb_dev_xxx")
        >>>
        >>> # Create a session context
        >>> session = client.create_session(
        ...     agent_id="agent_123",
        ...     context_type="conversation"
        ... )
        >>>
        >>> # Update context
        >>> client.update(session['id'], {"topic": "authentication"})
    """

    def create_session(
        self,
        agent_id: str,
        context_type: str = "conversation",
        initial_context: Optional[Dict[str, Any]] = None,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new context session.

        Args:
            agent_id: Unique identifier for the agent
            context_type: Type of context (conversation, task, workflow)
            initial_context: Initial context data (optional)
            ttl_seconds: Session time-to-live (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing created session

        Example:
            >>> session = client.create_session(
            ...     agent_id="agent_123",
            ...     context_type="task",
            ...     initial_context={
            ...         "task": "API integration",
            ...         "requirements": ["authentication", "rate limiting"]
            ...     }
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "context_type": context_type
        }

        if initial_context:
            payload["context"] = initial_context
        if ttl_seconds:
            payload["ttl_seconds"] = ttl_seconds
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/context", json=payload)

    def get(self, session_id: str) -> Dict[str, Any]:
        """
        Get the current context for a session.

        Args:
            session_id: ID of the session

        Returns:
            Dict containing session context

        Example:
            >>> context = client.get(session_id="sess_123")
            >>> print(f"Current topic: {context['data']['topic']}")
        """
        if not session_id:
            raise ValueError("session_id is required")

        return self._request("GET", f"/api/autonomous/context/{session_id}")

    def update(
        self,
        session_id: str,
        context_data: Dict[str, Any],
        merge: bool = True
    ) -> Dict[str, Any]:
        """
        Update session context.

        Args:
            session_id: ID of the session
            context_data: New context data
            merge: Merge with existing context (default: True)

        Returns:
            Dict containing updated context

        Example:
            >>> client.update(
            ...     session_id="sess_123",
            ...     context_data={
            ...         "current_step": "authentication",
            ...         "progress": 0.5
            ...     }
            ... )
        """
        if not session_id:
            raise ValueError("session_id is required")
        if not context_data:
            raise ValueError("context_data is required")

        return self._request(
            "PUT",
            f"/api/autonomous/context/{session_id}",
            json={"context": context_data, "merge": merge}
        )

    def add_to_history(
        self,
        session_id: str,
        entry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add an entry to the session history.

        Args:
            session_id: ID of the session
            entry: History entry to add

        Returns:
            Dict containing updated history

        Example:
            >>> client.add_to_history(
            ...     session_id="sess_123",
            ...     entry={
            ...         "action": "user_message",
            ...         "content": "User asked about authentication"
            ...     }
            ... )
        """
        if not session_id:
            raise ValueError("session_id is required")
        if not entry:
            raise ValueError("entry is required")

        return self._request(
            "POST",
            f"/api/autonomous/context/{session_id}/history",
            json={"entry": entry}
        )

    def get_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get session history.

        Args:
            session_id: ID of the session
            limit: Maximum number of entries (default: 50)

        Returns:
            Dict containing history entries

        Example:
            >>> history = client.get_history(session_id="sess_123")
            >>> for entry in history['entries']:
            ...     print(f"{entry['timestamp']}: {entry['action']}")
        """
        if not session_id:
            raise ValueError("session_id is required")

        return self._request(
            "GET",
            f"/api/autonomous/context/{session_id}/history",
            params={"limit": limit}
        )

    def list_sessions(
        self,
        agent_id: str,
        active_only: bool = True,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List sessions for an agent.

        Args:
            agent_id: Unique identifier for the agent
            active_only: Only return active sessions (default: True)
            limit: Maximum number of sessions (default: 20)

        Returns:
            Dict containing list of sessions

        Example:
            >>> sessions = client.list_sessions(agent_id="agent_123")
            >>> for sess in sessions['sessions']:
            ...     print(f"{sess['id']}: {sess['context_type']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/context",
            params={
                "agent_id": agent_id,
                "active_only": active_only,
                "limit": limit
            }
        )

    def end_session(
        self,
        session_id: str,
        summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        End a context session.

        Args:
            session_id: ID of the session
            summary: Session summary (optional)

        Returns:
            Dict containing ended session info

        Example:
            >>> client.end_session(
            ...     session_id="sess_123",
            ...     summary="Completed API integration discussion"
            ... )
        """
        if not session_id:
            raise ValueError("session_id is required")

        payload = {"status": "ended"}
        if summary:
            payload["summary"] = self._sanitize_input(summary)

        return self._request(
            "PUT",
            f"/api/autonomous/context/{session_id}",
            json=payload
        )

    def get_environment(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent's environmental context.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing environment information

        Example:
            >>> env = client.get_environment(agent_id="agent_123")
            >>> print(f"Timezone: {env['timezone']}")
            >>> print(f"Locale: {env['locale']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/context/environment",
            params={"agent_id": agent_id}
        )

    def set_environment(
        self,
        agent_id: str,
        environment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set agent's environmental context.

        Args:
            agent_id: Unique identifier for the agent
            environment: Environment configuration

        Returns:
            Dict containing updated environment

        Example:
            >>> client.set_environment(
            ...     agent_id="agent_123",
            ...     environment={
            ...         "timezone": "America/New_York",
            ...         "locale": "en-US",
            ...         "capabilities": ["code_execution", "web_search"]
            ...     }
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not environment:
            raise ValueError("environment is required")

        return self._request(
            "PUT",
            "/api/autonomous/context/environment",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "environment": environment
            }
        )
