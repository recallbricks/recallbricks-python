"""
UncertaintyClient for RecallBricks Autonomous Agent API
Manages agent uncertainty quantification and confidence calibration
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class UncertaintyClient(BaseAutonomousClient):
    """
    Client for managing agent uncertainty and confidence.

    Enables agents to track, quantify, and calibrate their confidence levels,
    supporting better decision-making under uncertainty.

    Usage:
        >>> from recallbricks.autonomous import UncertaintyClient
        >>> client = UncertaintyClient(api_key="rb_dev_xxx")
        >>>
        >>> # Record uncertainty
        >>> client.record(
        ...     agent_id="agent_123",
        ...     topic="Authentication approach",
        ...     confidence=0.7,
        ...     reasoning="JWT is common but OAuth might be better for enterprise"
        ... )
        >>>
        >>> # Get uncertainty summary
        >>> summary = client.get_summary(agent_id="agent_123")
    """

    def record(
        self,
        agent_id: str,
        topic: str,
        confidence: float,
        reasoning: Optional[str] = None,
        factors: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record an uncertainty measurement.

        Args:
            agent_id: Unique identifier for the agent
            topic: Topic or decision being evaluated
            confidence: Confidence level 0.0-1.0
            reasoning: Explanation of confidence level (optional)
            factors: Factors affecting confidence (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing recorded uncertainty

        Example:
            >>> client.record(
            ...     agent_id="agent_123",
            ...     topic="Database choice",
            ...     confidence=0.6,
            ...     reasoning="PostgreSQL is proven but MongoDB might scale better",
            ...     factors=[
            ...         {"name": "experience", "impact": 0.3},
            ...         {"name": "research", "impact": 0.2}
            ...     ]
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not topic:
            raise ValueError("topic is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "topic": self._sanitize_input(topic),
            "confidence": max(0.0, min(1.0, confidence))
        }

        if reasoning:
            payload["reasoning"] = self._sanitize_input(reasoning)
        if factors:
            payload["factors"] = factors
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/uncertainty", json=payload)

    def get_by_topic(
        self,
        agent_id: str,
        topic: str
    ) -> Dict[str, Any]:
        """
        Get uncertainty records for a specific topic.

        Args:
            agent_id: Unique identifier for the agent
            topic: Topic to query

        Returns:
            Dict containing uncertainty history for the topic

        Example:
            >>> history = client.get_by_topic(
            ...     agent_id="agent_123",
            ...     topic="Authentication approach"
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not topic:
            raise ValueError("topic is required")

        return self._request(
            "GET",
            "/api/autonomous/uncertainty/topic",
            params={"agent_id": agent_id, "topic": topic}
        )

    def get_summary(
        self,
        agent_id: str,
        period: str = "7d"
    ) -> Dict[str, Any]:
        """
        Get uncertainty summary for an agent.

        Args:
            agent_id: Unique identifier for the agent
            period: Time period (1d, 7d, 30d)

        Returns:
            Dict containing uncertainty statistics

        Example:
            >>> summary = client.get_summary(agent_id="agent_123")
            >>> print(f"Avg confidence: {summary['avg_confidence']}")
            >>> print(f"High uncertainty topics: {summary['high_uncertainty_topics']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/uncertainty/summary",
            params={"agent_id": agent_id, "period": period}
        )

    def calibrate(
        self,
        agent_id: str,
        topic: str,
        actual_outcome: str,
        predicted_confidence: float
    ) -> Dict[str, Any]:
        """
        Calibrate confidence based on actual outcome.

        Args:
            agent_id: Unique identifier for the agent
            topic: Topic that was predicted
            actual_outcome: What actually happened
            predicted_confidence: The confidence that was predicted

        Returns:
            Dict containing calibration results

        Example:
            >>> result = client.calibrate(
            ...     agent_id="agent_123",
            ...     topic="JWT authentication",
            ...     actual_outcome="Worked well for the use case",
            ...     predicted_confidence=0.7
            ... )
            >>> print(f"Calibration adjustment: {result['adjustment']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not topic:
            raise ValueError("topic is required")

        return self._request(
            "POST",
            "/api/autonomous/uncertainty/calibrate",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "topic": self._sanitize_input(topic),
                "actual_outcome": self._sanitize_input(actual_outcome),
                "predicted_confidence": predicted_confidence
            }
        )

    def get_calibration_score(self, agent_id: str) -> Dict[str, Any]:
        """
        Get calibration score showing how well-calibrated the agent is.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing calibration metrics

        Example:
            >>> score = client.get_calibration_score(agent_id="agent_123")
            >>> print(f"Calibration score: {score['score']}")
            >>> print(f"Over-confident areas: {score['over_confident']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/uncertainty/calibration",
            params={"agent_id": agent_id}
        )

    def suggest_information_needs(
        self,
        agent_id: str,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Suggest areas where more information is needed.

        Args:
            agent_id: Unique identifier for the agent
            threshold: Confidence threshold below which info is needed

        Returns:
            Dict containing topics needing more information

        Example:
            >>> needs = client.suggest_information_needs(
            ...     agent_id="agent_123",
            ...     threshold=0.6
            ... )
            >>> for topic in needs['topics']:
            ...     print(f"{topic['name']}: {topic['current_confidence']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "POST",
            "/api/autonomous/uncertainty/needs",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "threshold": threshold
            }
        )

    def resolve(
        self,
        uncertainty_id: str,
        resolution: str,
        new_confidence: float
    ) -> Dict[str, Any]:
        """
        Resolve an uncertainty with new information.

        Args:
            uncertainty_id: ID of the uncertainty record
            resolution: How the uncertainty was resolved
            new_confidence: New confidence level after resolution

        Returns:
            Dict containing updated uncertainty record

        Example:
            >>> client.resolve(
            ...     uncertainty_id="unc_123",
            ...     resolution="Consulted with security team, JWT confirmed",
            ...     new_confidence=0.95
            ... )
        """
        if not uncertainty_id:
            raise ValueError("uncertainty_id is required")

        return self._request(
            "PUT",
            f"/api/autonomous/uncertainty/{uncertainty_id}",
            json={
                "resolution": self._sanitize_input(resolution),
                "new_confidence": max(0.0, min(1.0, new_confidence)),
                "status": "resolved"
            }
        )
