"""
MetacognitionClient for RecallBricks Autonomous Agent API
Enables agent self-awareness and reasoning about its own cognitive processes
"""

from typing import Dict, Any, Optional, List
from .base import BaseAutonomousClient


class MetacognitionClient(BaseAutonomousClient):
    """
    Client for agent metacognition capabilities.

    Metacognition enables AI agents to reason about their own thinking,
    monitor their cognitive processes, and improve decision-making.

    Usage:
        >>> from recallbricks.autonomous import MetacognitionClient
        >>> client = MetacognitionClient(api_key="rb_dev_xxx")
        >>>
        >>> # Log a reasoning step
        >>> client.log_reasoning(
        ...     agent_id="agent_123",
        ...     step="analyzing_requirements",
        ...     reasoning="User wants authentication, considering OAuth vs JWT"
        ... )
        >>>
        >>> # Evaluate decision confidence
        >>> confidence = client.evaluate_confidence(
        ...     agent_id="agent_123",
        ...     decision="Use JWT for authentication"
        ... )
    """

    def log_reasoning(
        self,
        agent_id: str,
        step: str,
        reasoning: str,
        confidence: float = 0.5,
        alternatives: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log a reasoning step for metacognitive tracking.

        Args:
            agent_id: Unique identifier for the agent
            step: Name/identifier of the reasoning step
            reasoning: Description of the reasoning process
            confidence: Confidence level 0.0-1.0 (default: 0.5)
            alternatives: Alternative approaches considered (optional)
            metadata: Additional metadata (optional)

        Returns:
            Dict containing logged reasoning entry

        Example:
            >>> client.log_reasoning(
            ...     agent_id="agent_123",
            ...     step="solution_selection",
            ...     reasoning="Chose React over Vue due to team familiarity",
            ...     confidence=0.8,
            ...     alternatives=["Vue.js", "Svelte"]
            ... )
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not step:
            raise ValueError("step is required")
        if not reasoning:
            raise ValueError("reasoning is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "step": self._sanitize_input(step, max_length=256),
            "reasoning": self._sanitize_input(reasoning),
            "confidence": max(0.0, min(1.0, confidence))
        }

        if alternatives:
            payload["alternatives"] = alternatives
        if metadata:
            payload["metadata"] = metadata

        return self._request("POST", "/api/autonomous/metacognition/reasoning", json=payload)

    def evaluate_confidence(
        self,
        agent_id: str,
        decision: str,
        context: Optional[str] = None,
        evidence: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate confidence in a decision.

        Args:
            agent_id: Unique identifier for the agent
            decision: The decision to evaluate
            context: Context for the decision (optional)
            evidence: Supporting evidence (optional)

        Returns:
            Dict containing confidence evaluation

        Example:
            >>> result = client.evaluate_confidence(
            ...     agent_id="agent_123",
            ...     decision="Deploy to production",
            ...     context="All tests passing, staging verified",
            ...     evidence=["100% test coverage", "QA approval"]
            ... )
            >>> print(f"Confidence: {result['confidence']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not decision:
            raise ValueError("decision is required")

        payload = {
            "agent_id": self._sanitize_input(agent_id, max_length=256),
            "decision": self._sanitize_input(decision)
        }

        if context:
            payload["context"] = self._sanitize_input(context)
        if evidence:
            payload["evidence"] = evidence

        return self._request("POST", "/api/autonomous/metacognition/evaluate", json=payload)

    def get_reasoning_trace(
        self,
        agent_id: str,
        session_id: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get the reasoning trace for an agent.

        Args:
            agent_id: Unique identifier for the agent
            session_id: Filter by specific session (optional)
            limit: Maximum number of entries (default: 20)

        Returns:
            Dict containing reasoning trace

        Example:
            >>> trace = client.get_reasoning_trace(agent_id="agent_123")
            >>> for entry in trace['entries']:
            ...     print(f"{entry['step']}: {entry['reasoning']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        params = {"agent_id": agent_id, "limit": limit}
        if session_id:
            params["session_id"] = session_id

        return self._request("GET", "/api/autonomous/metacognition/trace", params=params)

    def analyze_patterns(
        self,
        agent_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze metacognitive patterns over time.

        Args:
            agent_id: Unique identifier for the agent
            days: Number of days to analyze (default: 7)

        Returns:
            Dict containing pattern analysis

        Example:
            >>> patterns = client.analyze_patterns(agent_id="agent_123", days=30)
            >>> print(f"Avg confidence: {patterns['avg_confidence']}")
            >>> print(f"Common biases: {patterns['detected_biases']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "POST",
            "/api/autonomous/metacognition/analyze",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "days": days
            }
        )

    def get_biases(self, agent_id: str) -> Dict[str, Any]:
        """
        Get detected cognitive biases for an agent.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Dict containing detected biases and mitigation suggestions

        Example:
            >>> biases = client.get_biases(agent_id="agent_123")
            >>> for bias in biases['detected']:
            ...     print(f"{bias['type']}: {bias['description']}")
            ...     print(f"Mitigation: {bias['mitigation']}")
        """
        if not agent_id:
            raise ValueError("agent_id is required")

        return self._request(
            "GET",
            "/api/autonomous/metacognition/biases",
            params={"agent_id": agent_id}
        )

    def self_reflect(
        self,
        agent_id: str,
        topic: str,
        depth: str = "standard"
    ) -> Dict[str, Any]:
        """
        Trigger agent self-reflection on a topic.

        Args:
            agent_id: Unique identifier for the agent
            topic: Topic for self-reflection
            depth: Reflection depth (brief, standard, deep)

        Returns:
            Dict containing self-reflection results

        Example:
            >>> reflection = client.self_reflect(
            ...     agent_id="agent_123",
            ...     topic="Recent decision-making quality",
            ...     depth="deep"
            ... )
            >>> print(reflection['insights'])
        """
        if not agent_id:
            raise ValueError("agent_id is required")
        if not topic:
            raise ValueError("topic is required")

        return self._request(
            "POST",
            "/api/autonomous/metacognition/reflect",
            json={
                "agent_id": self._sanitize_input(agent_id, max_length=256),
                "topic": self._sanitize_input(topic),
                "depth": depth
            }
        )
