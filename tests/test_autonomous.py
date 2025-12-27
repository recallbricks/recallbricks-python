"""
Comprehensive tests for RecallBricks Autonomous Agent SDK
Tests all 9 autonomous clients and their methods
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json

from recallbricks.autonomous import (
    BaseAutonomousClient,
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
from recallbricks.exceptions import (
    AuthenticationError,
    ValidationError,
    RateLimitError,
    APIError,
    NotFoundError,
    RecallBricksError,
)


class TestBaseAutonomousClient(unittest.TestCase):
    """Test base autonomous client functionality"""

    def test_init_requires_api_key(self):
        """Test that api_key is required"""
        with self.assertRaises(AuthenticationError):
            BaseAutonomousClient(api_key=None)

    def test_init_sets_headers(self):
        """Test that headers are set correctly"""
        client = BaseAutonomousClient(api_key="test_key")
        self.assertEqual(client.session.headers["X-API-Key"], "test_key")
        self.assertEqual(client.session.headers["Content-Type"], "application/json")

    def test_init_custom_base_url(self):
        """Test custom base URL"""
        client = BaseAutonomousClient(
            api_key="test_key",
            base_url="https://custom.api.com/"
        )
        self.assertEqual(client.base_url, "https://custom.api.com")

    def test_sanitize_input(self):
        """Test input sanitization"""
        client = BaseAutonomousClient(api_key="test_key")

        # Test normal string
        self.assertEqual(client._sanitize_input("hello"), "hello")

        # Test max length
        long_string = "a" * 20000
        sanitized = client._sanitize_input(long_string, max_length=100)
        self.assertEqual(len(sanitized), 100)

        # Test control character removal
        with_control = "hello\x00world"
        sanitized = client._sanitize_input(with_control)
        self.assertEqual(sanitized, "helloworld")

    def test_sanitize_input_type_error(self):
        """Test sanitize_input raises TypeError for non-strings"""
        client = BaseAutonomousClient(api_key="test_key")
        with self.assertRaises(TypeError):
            client._sanitize_input(123)


class TestWorkingMemoryClient(unittest.TestCase):
    """Test WorkingMemoryClient"""

    def setUp(self):
        self.client = WorkingMemoryClient(api_key="test_key")

    @patch.object(WorkingMemoryClient, '_request')
    def test_store(self, mock_request):
        """Test store method"""
        mock_request.return_value = {"id": "mem_123", "content": "test"}

        result = self.client.store(
            agent_id="agent_123",
            content="Test content",
            memory_type="context",
            priority=0.8
        )

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertEqual(call_args[0][1], "/api/autonomous/working-memory")

    @patch.object(WorkingMemoryClient, '_request')
    def test_retrieve(self, mock_request):
        """Test retrieve method"""
        mock_request.return_value = {"memories": [], "count": 0}

        result = self.client.retrieve(agent_id="agent_123", limit=5)

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "GET")

    @patch.object(WorkingMemoryClient, '_request')
    def test_update(self, mock_request):
        """Test update method"""
        mock_request.return_value = {"id": "mem_123", "content": "updated"}

        result = self.client.update(memory_id="mem_123", content="new content")

        mock_request.assert_called_once()

    @patch.object(WorkingMemoryClient, '_request')
    def test_delete(self, mock_request):
        """Test delete method"""
        mock_request.return_value = {"deleted": True}

        result = self.client.delete(memory_id="mem_123")

        mock_request.assert_called_once()

    @patch.object(WorkingMemoryClient, '_request')
    def test_clear(self, mock_request):
        """Test clear method"""
        mock_request.return_value = {"deleted_count": 5}

        result = self.client.clear(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(WorkingMemoryClient, '_request')
    def test_consolidate(self, mock_request):
        """Test consolidate method"""
        mock_request.return_value = {"consolidated_count": 3}

        result = self.client.consolidate(agent_id="agent_123", strategy="importance")

        mock_request.assert_called_once()

    def test_store_requires_agent_id(self):
        """Test that store requires agent_id"""
        with self.assertRaises(ValueError):
            self.client.store(agent_id="", content="test")

    def test_store_requires_content(self):
        """Test that store requires content"""
        with self.assertRaises(ValueError):
            self.client.store(agent_id="agent_123", content="")


class TestProspectiveMemoryClient(unittest.TestCase):
    """Test ProspectiveMemoryClient"""

    def setUp(self):
        self.client = ProspectiveMemoryClient(api_key="test_key")

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_create(self, mock_request):
        """Test create method"""
        mock_request.return_value = {"id": "pm_123", "content": "reminder"}

        result = self.client.create(
            agent_id="agent_123",
            content="Follow up",
            trigger_type="time",
            trigger_at="2024-12-28T10:00:00Z"
        )

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_get(self, mock_request):
        """Test get method"""
        mock_request.return_value = {"id": "pm_123"}

        result = self.client.get(memory_id="pm_123")

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_get_pending(self, mock_request):
        """Test get_pending method"""
        mock_request.return_value = {"memories": []}

        result = self.client.get_pending(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_check_triggers(self, mock_request):
        """Test check_triggers method"""
        mock_request.return_value = {"triggered": []}

        result = self.client.check_triggers(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_mark_completed(self, mock_request):
        """Test mark_completed method"""
        mock_request.return_value = {"status": "completed"}

        result = self.client.mark_completed(memory_id="pm_123", outcome="Done")

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_cancel(self, mock_request):
        """Test cancel method"""
        mock_request.return_value = {"status": "cancelled"}

        result = self.client.cancel(memory_id="pm_123", reason="No longer needed")

        mock_request.assert_called_once()

    @patch.object(ProspectiveMemoryClient, '_request')
    def test_reschedule(self, mock_request):
        """Test reschedule method"""
        mock_request.return_value = {"trigger_at": "2024-12-29T10:00:00Z"}

        result = self.client.reschedule(
            memory_id="pm_123",
            trigger_at="2024-12-29T10:00:00Z"
        )

        mock_request.assert_called_once()


class TestMetacognitionClient(unittest.TestCase):
    """Test MetacognitionClient"""

    def setUp(self):
        self.client = MetacognitionClient(api_key="test_key")

    @patch.object(MetacognitionClient, '_request')
    def test_log_reasoning(self, mock_request):
        """Test log_reasoning method"""
        mock_request.return_value = {"id": "r_123"}

        result = self.client.log_reasoning(
            agent_id="agent_123",
            step="decision",
            reasoning="Chose option A",
            confidence=0.8
        )

        mock_request.assert_called_once()

    @patch.object(MetacognitionClient, '_request')
    def test_evaluate_confidence(self, mock_request):
        """Test evaluate_confidence method"""
        mock_request.return_value = {"confidence": 0.85}

        result = self.client.evaluate_confidence(
            agent_id="agent_123",
            decision="Use PostgreSQL"
        )

        mock_request.assert_called_once()

    @patch.object(MetacognitionClient, '_request')
    def test_get_reasoning_trace(self, mock_request):
        """Test get_reasoning_trace method"""
        mock_request.return_value = {"entries": []}

        result = self.client.get_reasoning_trace(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(MetacognitionClient, '_request')
    def test_analyze_patterns(self, mock_request):
        """Test analyze_patterns method"""
        mock_request.return_value = {"patterns": []}

        result = self.client.analyze_patterns(agent_id="agent_123", days=7)

        mock_request.assert_called_once()

    @patch.object(MetacognitionClient, '_request')
    def test_get_biases(self, mock_request):
        """Test get_biases method"""
        mock_request.return_value = {"detected": []}

        result = self.client.get_biases(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(MetacognitionClient, '_request')
    def test_self_reflect(self, mock_request):
        """Test self_reflect method"""
        mock_request.return_value = {"insights": "test"}

        result = self.client.self_reflect(
            agent_id="agent_123",
            topic="decision quality",
            depth="deep"
        )

        mock_request.assert_called_once()


class TestMemoryTypesClient(unittest.TestCase):
    """Test MemoryTypesClient"""

    def setUp(self):
        self.client = MemoryTypesClient(api_key="test_key")

    @patch.object(MemoryTypesClient, '_request')
    def test_store_episodic(self, mock_request):
        """Test store_episodic method"""
        mock_request.return_value = {"id": "ep_123"}

        result = self.client.store_episodic(
            agent_id="agent_123",
            event="Fixed bug",
            importance=0.8
        )

        mock_request.assert_called_once()

    @patch.object(MemoryTypesClient, '_request')
    def test_store_semantic(self, mock_request):
        """Test store_semantic method"""
        mock_request.return_value = {"id": "sem_123"}

        result = self.client.store_semantic(
            agent_id="agent_123",
            fact="Python uses indentation",
            category="programming"
        )

        mock_request.assert_called_once()

    @patch.object(MemoryTypesClient, '_request')
    def test_store_procedural(self, mock_request):
        """Test store_procedural method"""
        mock_request.return_value = {"id": "proc_123"}

        result = self.client.store_procedural(
            agent_id="agent_123",
            skill="Deploy to production",
            steps=["Build", "Test", "Deploy"]
        )

        mock_request.assert_called_once()

    @patch.object(MemoryTypesClient, '_request')
    def test_retrieve(self, mock_request):
        """Test retrieve method"""
        mock_request.return_value = {"memories": []}

        result = self.client.retrieve(agent_id="agent_123", memory_type="semantic")

        mock_request.assert_called_once()

    @patch.object(MemoryTypesClient, '_request')
    def test_get_statistics(self, mock_request):
        """Test get_statistics method"""
        mock_request.return_value = {"episodic": {"count": 5}}

        result = self.client.get_statistics(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(MemoryTypesClient, '_request')
    def test_consolidate_semantic(self, mock_request):
        """Test consolidate_semantic method"""
        mock_request.return_value = {"merged_count": 3}

        result = self.client.consolidate_semantic(agent_id="agent_123")

        mock_request.assert_called_once()


class TestGoalsClient(unittest.TestCase):
    """Test GoalsClient"""

    def setUp(self):
        self.client = GoalsClient(api_key="test_key")

    @patch.object(GoalsClient, '_request')
    def test_create(self, mock_request):
        """Test create method"""
        mock_request.return_value = {"id": "goal_123"}

        result = self.client.create(
            agent_id="agent_123",
            title="Implement OAuth"
        )

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_get(self, mock_request):
        """Test get method"""
        mock_request.return_value = {"id": "goal_123", "title": "Test"}

        result = self.client.get(goal_id="goal_123")

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_list(self, mock_request):
        """Test list method"""
        mock_request.return_value = {"goals": []}

        result = self.client.list(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_update_progress(self, mock_request):
        """Test update_progress method"""
        mock_request.return_value = {"progress": 50}

        result = self.client.update_progress(goal_id="goal_123", progress=50)

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_add_subgoal(self, mock_request):
        """Test add_subgoal method"""
        mock_request.side_effect = [
            {"id": "goal_123", "agent_id": "agent_123"},  # get parent
            {"id": "subgoal_456"}  # create subgoal
        ]

        result = self.client.add_subgoal(
            parent_goal_id="goal_123",
            title="Write tests"
        )

        self.assertEqual(mock_request.call_count, 2)

    @patch.object(GoalsClient, '_request')
    def test_complete(self, mock_request):
        """Test complete method"""
        mock_request.return_value = {"status": "completed"}

        result = self.client.complete(goal_id="goal_123", outcome="Success")

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_cancel(self, mock_request):
        """Test cancel method"""
        mock_request.return_value = {"status": "cancelled"}

        result = self.client.cancel(goal_id="goal_123", reason="Changed")

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_get_hierarchy(self, mock_request):
        """Test get_hierarchy method"""
        mock_request.return_value = {"subgoals": []}

        result = self.client.get_hierarchy(goal_id="goal_123")

        mock_request.assert_called_once()

    @patch.object(GoalsClient, '_request')
    def test_suggest_next_steps(self, mock_request):
        """Test suggest_next_steps method"""
        mock_request.return_value = {"steps": []}

        result = self.client.suggest_next_steps(goal_id="goal_123")

        mock_request.assert_called_once()


class TestHealthClient(unittest.TestCase):
    """Test HealthClient"""

    def setUp(self):
        self.client = HealthClient(api_key="test_key")

    @patch.object(HealthClient, '_request')
    def test_check(self, mock_request):
        """Test check method"""
        mock_request.return_value = {"status": "healthy"}

        result = self.client.check(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_get_metrics(self, mock_request):
        """Test get_metrics method"""
        mock_request.return_value = {"avg_response_time": 100}

        result = self.client.get_metrics(agent_id="agent_123", period="24h")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_get_memory_usage(self, mock_request):
        """Test get_memory_usage method"""
        mock_request.return_value = {"working_memory": {"count": 10}}

        result = self.client.get_memory_usage(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_get_error_log(self, mock_request):
        """Test get_error_log method"""
        mock_request.return_value = {"entries": []}

        result = self.client.get_error_log(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_run_diagnostics(self, mock_request):
        """Test run_diagnostics method"""
        mock_request.return_value = {"checks": []}

        result = self.client.run_diagnostics(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_get_quota_status(self, mock_request):
        """Test get_quota_status method"""
        mock_request.return_value = {"api_calls": {"used": 100}}

        result = self.client.get_quota_status(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_ping(self, mock_request):
        """Test ping method"""
        mock_request.return_value = {"status": "ok"}

        result = self.client.ping()

        mock_request.assert_called_once()

    @patch.object(HealthClient, '_request')
    def test_get_uptime(self, mock_request):
        """Test get_uptime method"""
        mock_request.return_value = {"percentage": 99.9}

        result = self.client.get_uptime(agent_id="agent_123")

        mock_request.assert_called_once()


class TestUncertaintyClient(unittest.TestCase):
    """Test UncertaintyClient"""

    def setUp(self):
        self.client = UncertaintyClient(api_key="test_key")

    @patch.object(UncertaintyClient, '_request')
    def test_record(self, mock_request):
        """Test record method"""
        mock_request.return_value = {"id": "unc_123"}

        result = self.client.record(
            agent_id="agent_123",
            topic="Database choice",
            confidence=0.6
        )

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_get_by_topic(self, mock_request):
        """Test get_by_topic method"""
        mock_request.return_value = {"history": []}

        result = self.client.get_by_topic(
            agent_id="agent_123",
            topic="Database choice"
        )

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_get_summary(self, mock_request):
        """Test get_summary method"""
        mock_request.return_value = {"avg_confidence": 0.7}

        result = self.client.get_summary(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_calibrate(self, mock_request):
        """Test calibrate method"""
        mock_request.return_value = {"adjustment": 0.1}

        result = self.client.calibrate(
            agent_id="agent_123",
            topic="Database choice",
            actual_outcome="Worked well",
            predicted_confidence=0.6
        )

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_get_calibration_score(self, mock_request):
        """Test get_calibration_score method"""
        mock_request.return_value = {"score": 0.85}

        result = self.client.get_calibration_score(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_suggest_information_needs(self, mock_request):
        """Test suggest_information_needs method"""
        mock_request.return_value = {"topics": []}

        result = self.client.suggest_information_needs(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(UncertaintyClient, '_request')
    def test_resolve(self, mock_request):
        """Test resolve method"""
        mock_request.return_value = {"status": "resolved"}

        result = self.client.resolve(
            uncertainty_id="unc_123",
            resolution="Confirmed approach",
            new_confidence=0.95
        )

        mock_request.assert_called_once()


class TestContextClient(unittest.TestCase):
    """Test ContextClient"""

    def setUp(self):
        self.client = ContextClient(api_key="test_key")

    @patch.object(ContextClient, '_request')
    def test_create_session(self, mock_request):
        """Test create_session method"""
        mock_request.return_value = {"id": "sess_123"}

        result = self.client.create_session(
            agent_id="agent_123",
            context_type="conversation"
        )

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_get(self, mock_request):
        """Test get method"""
        mock_request.return_value = {"data": {}}

        result = self.client.get(session_id="sess_123")

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_update(self, mock_request):
        """Test update method"""
        mock_request.return_value = {"updated": True}

        result = self.client.update(
            session_id="sess_123",
            context_data={"topic": "auth"}
        )

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_add_to_history(self, mock_request):
        """Test add_to_history method"""
        mock_request.return_value = {"added": True}

        result = self.client.add_to_history(
            session_id="sess_123",
            entry={"action": "user_message"}
        )

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_get_history(self, mock_request):
        """Test get_history method"""
        mock_request.return_value = {"entries": []}

        result = self.client.get_history(session_id="sess_123")

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_list_sessions(self, mock_request):
        """Test list_sessions method"""
        mock_request.return_value = {"sessions": []}

        result = self.client.list_sessions(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_end_session(self, mock_request):
        """Test end_session method"""
        mock_request.return_value = {"status": "ended"}

        result = self.client.end_session(session_id="sess_123")

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_get_environment(self, mock_request):
        """Test get_environment method"""
        mock_request.return_value = {"timezone": "UTC"}

        result = self.client.get_environment(agent_id="agent_123")

        mock_request.assert_called_once()

    @patch.object(ContextClient, '_request')
    def test_set_environment(self, mock_request):
        """Test set_environment method"""
        mock_request.return_value = {"updated": True}

        result = self.client.set_environment(
            agent_id="agent_123",
            environment={"timezone": "America/New_York"}
        )

        mock_request.assert_called_once()


class TestSearchClient(unittest.TestCase):
    """Test SearchClient"""

    def setUp(self):
        self.client = SearchClient(api_key="test_key")

    @patch.object(SearchClient, '_request')
    def test_semantic(self, mock_request):
        """Test semantic method"""
        mock_request.return_value = {"results": []}

        result = self.client.semantic(
            agent_id="agent_123",
            query="authentication"
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_filtered(self, mock_request):
        """Test filtered method"""
        mock_request.return_value = {"results": []}

        result = self.client.filtered(
            agent_id="agent_123",
            query="security",
            filters={"memory_type": "semantic"}
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_hybrid(self, mock_request):
        """Test hybrid method"""
        mock_request.return_value = {"results": []}

        result = self.client.hybrid(
            agent_id="agent_123",
            query="JWT token"
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_similar(self, mock_request):
        """Test similar method"""
        mock_request.return_value = {"results": []}

        result = self.client.similar(
            agent_id="agent_123",
            memory_id="mem_456"
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_temporal(self, mock_request):
        """Test temporal method"""
        mock_request.return_value = {"results": []}

        result = self.client.temporal(
            agent_id="agent_123",
            start_time="2024-12-01T00:00:00Z"
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_aggregate(self, mock_request):
        """Test aggregate method"""
        mock_request.return_value = {"buckets": []}

        result = self.client.aggregate(
            agent_id="agent_123",
            group_by="category"
        )

        mock_request.assert_called_once()

    @patch.object(SearchClient, '_request')
    def test_suggest(self, mock_request):
        """Test suggest method"""
        mock_request.return_value = {"suggestions": []}

        result = self.client.suggest(
            agent_id="agent_123",
            partial_query="auth"
        )

        mock_request.assert_called_once()


class TestValidationErrors(unittest.TestCase):
    """Test validation error handling across all clients"""

    def test_working_memory_validation(self):
        """Test WorkingMemoryClient validation"""
        client = WorkingMemoryClient(api_key="test_key")

        with self.assertRaises(ValueError):
            client.store(agent_id="", content="test")

        with self.assertRaises(ValueError):
            client.retrieve(agent_id="")

        with self.assertRaises(ValueError):
            client.update(memory_id="", content="test")

        with self.assertRaises(ValueError):
            client.update(memory_id="mem_123")  # No fields to update

    def test_prospective_memory_validation(self):
        """Test ProspectiveMemoryClient validation"""
        client = ProspectiveMemoryClient(api_key="test_key")

        with self.assertRaises(ValueError):
            client.create(agent_id="", content="test")

        with self.assertRaises(ValueError):
            client.get(memory_id="")

    def test_metacognition_validation(self):
        """Test MetacognitionClient validation"""
        client = MetacognitionClient(api_key="test_key")

        with self.assertRaises(ValueError):
            client.log_reasoning(agent_id="", step="test", reasoning="test")

        with self.assertRaises(ValueError):
            client.log_reasoning(agent_id="agent_123", step="", reasoning="test")

    def test_goals_validation(self):
        """Test GoalsClient validation"""
        client = GoalsClient(api_key="test_key")

        with self.assertRaises(ValueError):
            client.create(agent_id="", title="test")

        with self.assertRaises(ValueError):
            client.get(goal_id="")

    def test_search_validation(self):
        """Test SearchClient validation"""
        client = SearchClient(api_key="test_key")

        with self.assertRaises(ValueError):
            client.semantic(agent_id="", query="test")

        with self.assertRaises(ValueError):
            client.semantic(agent_id="agent_123", query="")


class TestPriorityBounds(unittest.TestCase):
    """Test priority value clamping"""

    @patch.object(WorkingMemoryClient, '_request')
    def test_priority_clamped_to_bounds(self, mock_request):
        """Test that priority is clamped between 0 and 1"""
        mock_request.return_value = {"id": "mem_123"}
        client = WorkingMemoryClient(api_key="test_key")

        # Test priority > 1 is clamped
        client.store(agent_id="agent_123", content="test", priority=1.5)
        call_args = mock_request.call_args
        payload = call_args[1]['json']
        self.assertEqual(payload['priority'], 1.0)

        # Test priority < 0 is clamped
        client.store(agent_id="agent_123", content="test", priority=-0.5)
        call_args = mock_request.call_args
        payload = call_args[1]['json']
        self.assertEqual(payload['priority'], 0.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
