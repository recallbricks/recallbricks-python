"""
GoalsClient for RecallBricks Autonomous Agent API
Manages agent goals, objectives, and progress tracking
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class GoalsClient(BaseAutonomousClient):
    """
    Client for managing agent goals and objectives.

    Enables agents to set, track, and achieve hierarchical goals,
    supporting long-term planning and autonomous behavior.

    Usage:
        >>> from recallbricks.autonomous import GoalsClient
        >>> client = GoalsClient(api_key="rb_dev_xxx")
        >>>
        >>> # Create a goal
        >>> goal = client.create(
        ...     agent_id="agent_123",
        ...     title="Complete API integration",
        ...     description="Integrate payment API with checkout flow"
        ... )
        >>>
        >>> # Add subgoals
        >>> client.add_subgoal(goal['id'], "Research API documentation")
        >>> client.add_subgoal(goal['id'], "Implement authentication")
    """

    def create(
        self,
        agent_id: str,
        title: str,
        description: Optional[str] = None,
        priority: float = 0.5,
        deadline: Optional[str] = None,
        parent_goal_id: Optional[str] = None,
        success_criteria: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new goal.

        Args:
            agent_id: Unique identifier for the agent
            title: Goal title
            description: Detailed description (optional)
            priority: Priority level 0.0-1.0 (default: 0.5)
            deadline: ISO timestamp deadline (optional)
            parent_goal_id: ID of parent goal for subgoals (optional)
            success_criteria: List of success criteria (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing created goal

        Example:
            >>> goal = client.create(
            ...     agent_id="agent_123",
            ...     title="Implement authentication",
            ...     description="Add JWT-based authentication to the API",
            ...     priority=0.9,
            ...     success_criteria=[
            ...         "Login endpoint works",
            ...         "Tokens are validated",
            ...         "Refresh tokens implemented"
            ...     ]
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not title:
            raise ValueError("title is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "title": self._sanitize_input(title, max_length=500),
            "priority": max(0.0, min(1.0, priority))
        }

        if description:
            payload["description"] = self._sanitize_input(description)
        if deadline:
            payload["deadline"] = deadline
        if parent_goal_id:
            payload["parent_goal_id"] = parent_goal_id
        if success_criteria:
            payload["success_criteria"] = success_criteria
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/goals", json=payload)

    def get(self, goal_id: str) -> Dict[str, Any]:
        """
        Get a specific goal by ID.

        Args:
            goal_id: ID of the goal

        Returns:
            Dict containing goal details

        Example:
            >>> goal = client.get(goal_id="goal_123")
            >>> print(f"{goal['title']}: {goal['progress']}%")
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        return self._request("GET", f"/api/autonomous/goals/{goal_id}")

    def list(
        self,
        agent_id: str,
        status: Optional[str] = None,
        include_subgoals: bool = True,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        List goals for an agent.

        Args:
            agent_id: Unique identifier for the agent
            status: Filter by status (active, completed, cancelled)
            include_subgoals: Include nested subgoals (default: True)
            limit: Maximum number of goals (default: 20)

        Returns:
            Dict containing list of goals

        Example:
            >>> goals = client.list(agent_id="agent_123", status="active")
            >>> for goal in goals['goals']:
            ...     print(f"{goal['title']}: {goal['progress']}%")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {
            "agent_id": agent_id,
            "include_subgoals": include_subgoals,
            "limit": limit
        }
        if status:
            params["status"] = status

        return self._request("GET", "/api/autonomous/goals", params=params)

    def update_progress(
        self,
        goal_id: str,
        progress: float,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update goal progress.

        Args:
            goal_id: ID of the goal
            progress: Progress percentage 0-100
            notes: Progress notes (optional)

        Returns:
            Dict containing updated goal

        Example:
            >>> client.update_progress(
            ...     goal_id="goal_123",
            ...     progress=75,
            ...     notes="Authentication complete, working on refresh tokens"
            ... )
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        payload = {"progress": max(0, min(100, progress))}
        if notes:
            payload["notes"] = self._sanitize_input(notes)

        return self._request("PUT", f"/api/autonomous/goals/{goal_id}", json=payload)

    def add_subgoal(
        self,
        parent_goal_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a subgoal to an existing goal.

        Args:
            parent_goal_id: ID of the parent goal
            title: Subgoal title
            description: Subgoal description (optional)

        Returns:
            Dict containing created subgoal

        Example:
            >>> subgoal = client.add_subgoal(
            ...     parent_goal_id="goal_123",
            ...     title="Write unit tests",
            ...     description="Test authentication endpoints"
            ... )
        """
        if not parent_goal_id:
            raise ValueError("parent_goal_id is required")
        if not title:
            raise ValueError("title is required")

        # First get the parent goal to get the agent_id
        parent = self.get(parent_goal_id)

        payload = {
            "agent_id": parent.get("agent_id"),
            "title": self._sanitize_input(title, max_length=500),
            "parent_goal_id": parent_goal_id
        }
        if description:
            payload["description"] = self._sanitize_input(description)

        return self._request("POST", "/api/autonomous/goals", json=payload)

    def complete(
        self,
        goal_id: str,
        outcome: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark a goal as completed.

        Args:
            goal_id: ID of the goal
            outcome: Outcome description (optional)

        Returns:
            Dict containing updated goal

        Example:
            >>> client.complete(
            ...     goal_id="goal_123",
            ...     outcome="Successfully implemented JWT authentication"
            ... )
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        payload = {"status": "completed", "progress": 100}
        if outcome:
            payload["outcome"] = self._sanitize_input(outcome)

        return self._request("PUT", f"/api/autonomous/goals/{goal_id}", json=payload)

    def cancel(
        self,
        goal_id: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a goal.

        Args:
            goal_id: ID of the goal
            reason: Cancellation reason (optional)

        Returns:
            Dict containing updated goal

        Example:
            >>> client.cancel(
            ...     goal_id="goal_123",
            ...     reason="Requirements changed"
            ... )
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        payload = {"status": "cancelled"}
        if reason:
            payload["reason"] = self._sanitize_input(reason)

        return self._request("PUT", f"/api/autonomous/goals/{goal_id}", json=payload)

    def get_hierarchy(self, goal_id: str) -> Dict[str, Any]:
        """
        Get the full goal hierarchy.

        Args:
            goal_id: ID of the root goal

        Returns:
            Dict containing goal tree with all subgoals

        Example:
            >>> hierarchy = client.get_hierarchy(goal_id="goal_123")
            >>> def print_tree(goal, indent=0):
            ...     print("  " * indent + goal['title'])
            ...     for sub in goal.get('subgoals', []):
            ...         print_tree(sub, indent + 1)
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        return self._request("GET", f"/api/autonomous/goals/{goal_id}/hierarchy")

    def suggest_next_steps(self, goal_id: str) -> Dict[str, Any]:
        """
        Get AI-suggested next steps for a goal.

        Args:
            goal_id: ID of the goal

        Returns:
            Dict containing suggested next steps

        Example:
            >>> suggestions = client.suggest_next_steps(goal_id="goal_123")
            >>> for step in suggestions['steps']:
            ...     print(f"- {step['action']}: {step['reasoning']}")
        """
        if not goal_id:
            raise ValueError("goal_id is required")

        return self._request("POST", f"/api/autonomous/goals/{goal_id}/suggest")
