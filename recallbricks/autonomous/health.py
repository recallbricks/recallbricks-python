"""
HealthClient for RecallBricks Autonomous Agent API
Monitors agent health, performance, and operational status
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class HealthClient(BaseAutonomousClient):
    """
    Client for monitoring agent health and performance.

    Provides health checks, performance metrics, and diagnostic capabilities
    for autonomous agents.

    Usage:
        >>> from recallbricks.autonomous import HealthClient
        >>> client = HealthClient(api_key="rb_dev_xxx")
        >>>
        >>> # Check agent health
        >>> health = client.check(agent_id="agent_123")
        >>> print(f"Status: {health['status']}")
        >>>
        >>> # Get performance metrics
        >>> metrics = client.get_metrics(agent_id="agent_123")
    """

    def check(self, agent_id: str) -> Dict[str, Any]:
        """
        Check overall health status of an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing health status and component statuses

        Example:
            >>> health = client.check(agent_id="agent_123")
            >>> print(f"Overall: {health['status']}")
            >>> for component, status in health['components'].items():
            ...     print(f"  {component}: {status['status']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/health",
            params={"agent_id": agent_id}
        )

    def get_metrics(
        self,
        agent_id: str,
        period: str = "1h",
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get performance metrics for an agent.

        Args:
            agent_id: Unique identifier for the agent
            period: Time period (1h, 24h, 7d, 30d)
            metrics: Specific metrics to retrieve (optional)

        Returns:
            Dict containing performance metrics

        Example:
            >>> metrics = client.get_metrics(
            ...     agent_id="agent_123",
            ...     period="24h"
            ... )
            >>> print(f"Avg response time: {metrics['avg_response_time']}ms")
            >>> print(f"Total requests: {metrics['total_requests']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {"agent_id": agent_id, "period": period}
        if metrics:
            params["metrics"] = ",".join(metrics)

        return self._request("GET", "/api/autonomous/health/metrics", params=params)

    def get_memory_usage(self, agent_id: str) -> Dict[str, Any]:
        """
        Get memory usage statistics for an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing memory usage by type

        Example:
            >>> usage = client.get_memory_usage(agent_id="agent_123")
            >>> print(f"Working memory: {usage['working_memory']['count']}")
            >>> print(f"Long-term memory: {usage['long_term']['count']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/health/memory",
            params={"agent_id": agent_id}
        )

    def get_error_log(
        self,
        agent_id: str,
        severity: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get error log for an agent.

        Args:
            agent_id: Unique identifier for the agent
            severity: Filter by severity (error, warning, info)
            limit: Maximum number of entries (default: 50)

        Returns:
            Dict containing error log entries

        Example:
            >>> errors = client.get_error_log(
            ...     agent_id="agent_123",
            ...     severity="error"
            ... )
            >>> for entry in errors['entries']:
            ...     print(f"[{entry['timestamp']}] {entry['message']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {"agent_id": agent_id, "limit": limit}
        if severity:
            params["severity"] = severity

        return self._request("GET", "/api/autonomous/health/errors", params=params)

    def run_diagnostics(self, agent_id: str) -> Dict[str, Any]:
        """
        Run full diagnostics on an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing diagnostic results

        Example:
            >>> diagnostics = client.run_diagnostics(agent_id="agent_123")
            >>> print(f"Overall: {diagnostics['overall_status']}")
            >>> for check in diagnostics['checks']:
            ...     print(f"{check['name']}: {check['status']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "POST",
            "/api/autonomous/health/diagnostics",
            json={"agent_id": self._sanitize_input(agent_id, max_length=256)}
        )

    def get_quota_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get quota and rate limit status for an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing quota information

        Example:
            >>> quota = client.get_quota_status(agent_id="agent_123")
            >>> print(f"API calls: {quota['api_calls']['used']}/{quota['api_calls']['limit']}")
            >>> print(f"Memory: {quota['memory']['used']}/{quota['memory']['limit']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/health/quota",
            params={"agent_id": agent_id}
        )

    def ping(self) -> Dict[str, Any]:
        """
        Simple health check for the autonomous API.

        Returns:
            Dict containing API status

        Example:
            >>> status = client.ping()
            >>> print(f"API Status: {status['status']}")
        """
        return self._request("GET", "/api/autonomous/health/ping")

    def get_uptime(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent uptime statistics.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing uptime information

        Example:
            >>> uptime = client.get_uptime(agent_id="agent_123")
            >>> print(f"Uptime: {uptime['percentage']}%")
            >>> print(f"Last restart: {uptime['last_restart']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/health/uptime",
            params={"agent_id": agent_id}
        )
