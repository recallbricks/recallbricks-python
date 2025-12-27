# RecallBricks Python SDK

**Enterprise-Grade Memory Layer for AI** - Persistent, intelligent memory across all AI models with advanced metacognition features and automatic metadata extraction.

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://pypi.org/project/recallbricks/)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Installation

```bash
pip install recallbricks
```

## Authentication

RecallBricks supports two authentication methods:

### 1. API Key (User-Level Access)
For individual users and development:

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")
```

### 2. Service Token (Server-to-Server Access)
For production services and server-to-server communication:

```python
from recallbricks import RecallBricks

rb = RecallBricks(service_token="rbk_service_xxx")
```

**Note:** You must provide either `api_key` or `service_token`, but not both.

## Quick Start (< 10 lines)

```python
from recallbricks import RecallBricks

# Option 1: API key authentication
rb = RecallBricks(api_key="rb_dev_xxx")

# Option 2: Service token authentication
# rb = RecallBricks(service_token="rbk_service_xxx")

# Learn memories with automatic metadata extraction (NEW!)
result = rb.learn("User prefers dark mode and TypeScript for frontend development")
print(f"Auto-tags: {result['metadata']['tags']}")
print(f"Category: {result['metadata']['category']}")

# Recall memories with organized results
results = rb.recall("user preferences", organized=True)
for category, info in results.get('categories', {}).items():
    print(f"{category}: {info['count']} memories")
```

## Features

### 🚀 Phase 2B: Automatic Metadata Extraction (NEW!)

RecallBricks now automatically extracts metadata from memories, reducing agent reasoning time from 10-15 seconds to 2-3 seconds (3-5x faster).

#### 1. **learn()** - Store Memories with Auto-Generated Metadata

The new `learn()` method automatically extracts tags, categories, entities, importance levels, and summaries:

```python
# Store a memory with automatic metadata extraction
result = rb.learn("Fixed authentication bug in the login flow using JWT refresh tokens")

print(f"ID: {result['id']}")
print(f"Auto-tags: {result['metadata']['tags']}")  # ['authentication', 'bug-fix', 'jwt', 'login']
print(f"Category: {result['metadata']['category']}")  # 'Development'
print(f"Entities: {result['metadata']['entities']}")  # ['JWT', 'authentication', 'login flow']
print(f"Importance: {result['metadata']['importance']}")  # 0.85
print(f"Summary: {result['metadata']['summary']}")  # 'Fixed auth bug using JWT refresh'
```

#### 2. **recall()** - Enhanced Search with Organized Results

The enhanced `recall()` method supports organized results with category summaries:

```python
# Basic recall (backward compatible)
results = rb.recall("authentication bugs", limit=10)
for mem in results['memories']:
    print(mem['text'])

# Organized recall with category summaries
results = rb.recall("user preferences", organized=True, min_helpfulness_score=0.5)

# Access memories
for mem in results['memories']:
    print(f"- {mem['text']} (score: {mem['score']})")
    print(f"  Category: {mem['metadata']['category']}")

# Access category summaries
for category, info in results['categories'].items():
    print(f"\n{category}:")
    print(f"  Count: {info['count']}")
    print(f"  Avg Score: {info['avg_score']:.2f}")
    print(f"  Summary: {info['summary']}")
```

#### 3. **Metadata Overrides**

You can override auto-generated metadata when needed:

```python
# Override specific metadata fields
result = rb.learn(
    "Important customer feedback about pricing",
    metadata={
        "tags": ["customer-feedback", "pricing", "urgent"],
        "category": "Customer Relations"
    }
)
```

### 🧠 Phase 2A: Metacognition & Intelligence

RecallBricks now includes advanced metacognition features that make your AI smarter about its own memory:

#### 1. **Predict Memories** - Proactive Memory Suggestions

Predict which memories might be useful based on context and recent usage patterns:

```python
# Predict memories based on what you're working on
predictions = rb.predict_memories(
    context="User is implementing authentication",
    recent_memory_ids=["mem_123", "mem_456"],  # Recently accessed
    limit=10
)

for pred in predictions:
    print(f"Predicted: {pred.content}")
    print(f"Confidence: {pred.confidence_score}")
    print(f"Reasoning: {pred.reasoning}")
```

#### 2. **Suggest Memories** - Context-Aware Recommendations

Get intelligent memory suggestions based on current context:

```python
# Get suggestions for current task
suggestions = rb.suggest_memories(
    context="Building a React authentication flow with JWT",
    limit=5,
    min_confidence=0.7,
    include_reasoning=True
)

for sug in suggestions:
    print(f"\n📌 {sug.content}")
    print(f"   Confidence: {sug.confidence:.2%}")
    print(f"   Why: {sug.reasoning}")
    print(f"   Context: {sug.relevance_context}")
```

#### 3. **Learning Metrics** - Understand Memory Performance

Analyze how your AI is learning and using memories:

```python
# Get learning metrics for the past 30 days
metrics = rb.get_learning_metrics(days=30)

print(f"Average Helpfulness: {metrics.avg_helpfulness:.2%}")
print(f"Total Usage: {metrics.total_usage}")
print(f"Active Memories: {metrics.active_memories}/{metrics.total_memories}")
print(f"Helpfulness Trend: {metrics.trends.helpfulness_trend}")
print(f"Usage Trend: {metrics.trends.usage_trend}")
print(f"Growth Rate: {metrics.trends.growth_rate:.2%}")
```

#### 4. **Pattern Analysis** - Discover Usage Patterns

Discover patterns in how memories are being used:

```python
# Analyze memory usage patterns
patterns = rb.get_patterns(days=14)

print(f"Summary: {patterns.summary}")
print(f"\nMost Useful Tags: {', '.join(patterns.most_useful_tags[:5])}")

print("\nFrequently Accessed Together:")
for pair in patterns.frequently_accessed_together[:3]:
    print(f"  - {pair[0]} ↔ {pair[1]}")

print("\nUnderutilized Memories:")
for mem in patterns.underutilized_memories[:5]:
    print(f"  - {mem['text']}")
```

#### 5. **Weighted Search** - Intelligent Search Ranking

Search with intelligent weighting based on usage, helpfulness, and recency:

```python
# Smart search with adaptive weighting
results = rb.search_weighted(
    query="authentication",
    limit=10,
    weight_by_usage=True,        # Boost frequently used memories
    decay_old_memories=True,      # Reduce score for old memories
    adaptive_weights=True,        # Use ML-based adaptive weighting
    min_helpfulness_score=0.7     # Filter by helpfulness
)

for result in results:
    print(f"\n🔍 {result.text}")
    print(f"   Relevance: {result.relevance_score:.2f}")
    print(f"   Usage Boost: +{result.usage_boost:.2f}")
    print(f"   Helpfulness: +{result.helpfulness_boost:.2f}")
    print(f"   Recency: +{result.recency_boost:.2f}")
    print(f"   Tags: {', '.join(result.tags)}")
```

### 🤖 Autonomous Agent Features (v1.3.0)

Build truly autonomous AI agents with specialized memory and cognition clients:

#### 1. **Working Memory** - Active Short-Term Context

```python
from recallbricks.autonomous import WorkingMemoryClient

working_memory = WorkingMemoryClient(api_key="rb_dev_xxx")

# Store context during a conversation
working_memory.store(
    agent_id="agent_123",
    content="User is asking about API authentication",
    memory_type="context",
    priority=0.8
)

# Retrieve active context
memories = working_memory.retrieve(agent_id="agent_123", limit=5)
for mem in memories['memories']:
    print(f"{mem['content']} (priority: {mem['priority']})")

# Consolidate important memories to long-term storage
working_memory.consolidate(agent_id="agent_123", strategy="importance")
```

#### 2. **Prospective Memory** - Future Tasks & Reminders

```python
from recallbricks.autonomous import ProspectiveMemoryClient

prospective = ProspectiveMemoryClient(api_key="rb_dev_xxx")

# Schedule a time-based reminder
reminder = prospective.create(
    agent_id="agent_123",
    content="Follow up with user about API integration",
    trigger_type="time",
    trigger_at="2024-12-28T10:00:00Z"
)

# Create an event-based trigger
prospective.create(
    agent_id="agent_123",
    content="Notify user when deployment completes",
    trigger_type="event",
    trigger_condition="deployment.status == 'completed'"
)

# Check for triggered reminders
triggered = prospective.check_triggers(agent_id="agent_123")
for mem in triggered['triggered']:
    print(f"Action needed: {mem['content']}")
```

#### 3. **Metacognition** - Self-Awareness & Reasoning

```python
from recallbricks.autonomous import MetacognitionClient

metacognition = MetacognitionClient(api_key="rb_dev_xxx")

# Log reasoning steps for transparency
metacognition.log_reasoning(
    agent_id="agent_123",
    step="solution_selection",
    reasoning="Chose JWT over OAuth for simplicity, given small team size",
    confidence=0.8,
    alternatives=["OAuth 2.0", "API Keys"]
)

# Evaluate confidence in a decision
confidence = metacognition.evaluate_confidence(
    agent_id="agent_123",
    decision="Use PostgreSQL for the database",
    context="High-traffic e-commerce application",
    evidence=["ACID compliance needed", "Complex queries required"]
)
print(f"Decision confidence: {confidence['confidence']}")

# Self-reflect on decision patterns
reflection = metacognition.self_reflect(
    agent_id="agent_123",
    topic="Recent technology choices",
    depth="deep"
)
print(f"Insights: {reflection['insights']}")
```

#### 4. **Memory Types** - Episodic, Semantic & Procedural

```python
from recallbricks.autonomous import MemoryTypesClient

memory_types = MemoryTypesClient(api_key="rb_dev_xxx")

# Store an episodic memory (event/experience)
memory_types.store_episodic(
    agent_id="agent_123",
    event="Successfully debugged authentication issue",
    context={"project": "api-server", "duration": "2 hours"},
    importance=0.8,
    emotions=["satisfaction", "relief"]
)

# Store semantic memory (fact/knowledge)
memory_types.store_semantic(
    agent_id="agent_123",
    fact="JWT tokens should be stored in httpOnly cookies",
    category="security",
    confidence=0.95,
    source="OWASP guidelines"
)

# Store procedural memory (skill/how-to)
memory_types.store_procedural(
    agent_id="agent_123",
    skill="Deploy to Kubernetes",
    steps=[
        "Run test suite",
        "Build Docker image",
        "Push to registry",
        "Update K8s deployment"
    ],
    proficiency=0.9
)
```

#### 5. **Goals** - Hierarchical Goal Management

```python
from recallbricks.autonomous import GoalsClient

goals = GoalsClient(api_key="rb_dev_xxx")

# Create a goal with success criteria
goal = goals.create(
    agent_id="agent_123",
    title="Implement OAuth integration",
    description="Add OAuth 2.0 authentication to the API",
    priority=0.9,
    success_criteria=[
        "Login flow works end-to-end",
        "Token refresh implemented",
        "All tests passing"
    ]
)

# Add subgoals
goals.add_subgoal(goal['id'], "Research OAuth providers")
goals.add_subgoal(goal['id'], "Implement authorization endpoint")
goals.add_subgoal(goal['id'], "Add token validation middleware")

# Track progress
goals.update_progress(goal['id'], progress=50, notes="OAuth flow complete")

# Get AI-suggested next steps
suggestions = goals.suggest_next_steps(goal['id'])
for step in suggestions['steps']:
    print(f"- {step['action']}: {step['reasoning']}")
```

#### 6. **Health Monitoring** - Agent Performance & Diagnostics

```python
from recallbricks.autonomous import HealthClient

health = HealthClient(api_key="rb_dev_xxx")

# Check overall agent health
status = health.check(agent_id="agent_123")
print(f"Status: {status['status']}")
for component, info in status['components'].items():
    print(f"  {component}: {info['status']}")

# Get performance metrics
metrics = health.get_metrics(agent_id="agent_123", period="24h")
print(f"Avg response time: {metrics['avg_response_time']}ms")

# Run full diagnostics
diagnostics = health.run_diagnostics(agent_id="agent_123")
for check in diagnostics['checks']:
    print(f"{check['name']}: {check['status']}")
```

#### 7. **Uncertainty Tracking** - Confidence Calibration

```python
from recallbricks.autonomous import UncertaintyClient

uncertainty = UncertaintyClient(api_key="rb_dev_xxx")

# Record uncertainty about a decision
uncertainty.record(
    agent_id="agent_123",
    topic="Database selection",
    confidence=0.6,
    reasoning="PostgreSQL is proven but MongoDB might scale better",
    factors=[
        {"name": "experience", "impact": 0.3},
        {"name": "research", "impact": 0.2}
    ]
)

# Calibrate based on actual outcomes
uncertainty.calibrate(
    agent_id="agent_123",
    topic="Database selection",
    actual_outcome="PostgreSQL handled scale well",
    predicted_confidence=0.6
)

# Get calibration score
score = uncertainty.get_calibration_score(agent_id="agent_123")
print(f"Calibration score: {score['score']}")
```

#### 8. **Context Management** - Session & Environment

```python
from recallbricks.autonomous import ContextClient

context = ContextClient(api_key="rb_dev_xxx")

# Create a conversation session
session = context.create_session(
    agent_id="agent_123",
    context_type="conversation",
    initial_context={"topic": "API design", "user_expertise": "intermediate"}
)

# Update context as conversation progresses
context.update(session['id'], {"current_focus": "authentication"})

# Track conversation history
context.add_to_history(session['id'], {
    "role": "user",
    "content": "How should I implement OAuth?"
})

# Set agent environment
context.set_environment(
    agent_id="agent_123",
    environment={
        "timezone": "America/New_York",
        "capabilities": ["code_execution", "web_search"]
    }
)
```

#### 9. **Advanced Search** - Semantic & Hybrid Search

```python
from recallbricks.autonomous import SearchClient

search = SearchClient(api_key="rb_dev_xxx")

# Semantic search across all memory types
results = search.semantic(
    agent_id="agent_123",
    query="authentication best practices",
    limit=10,
    min_score=0.7
)

# Hybrid search (keyword + semantic)
results = search.hybrid(
    agent_id="agent_123",
    query="JWT token security",
    keyword_weight=0.3,
    semantic_weight=0.7
)

# Find similar memories
similar = search.similar(
    agent_id="agent_123",
    memory_id="mem_456",
    limit=5
)

# Temporal search within a time range
results = search.temporal(
    agent_id="agent_123",
    start_time="2024-12-01T00:00:00Z",
    end_time="2024-12-27T23:59:59Z",
    query="security"
)
```

### 🔗 Relationship Support

Build connected knowledge graphs with memory relationships:

```python
# Save a memory
memory = rb.save("Fixed authentication bug in login flow")

# Get relationships for a memory
rels = rb.get_relationships(memory['id'])
print(f"Found {rels['count']} relationships")

# Get memory graph with relationships
graph = rb.get_graph_context(memory['id'], depth=2)
print(f"Graph contains {len(graph['nodes'])} connected memories")

# Search with relationships included
results = rb.search("authentication", include_relationships=True)
for result in results:
    if result.get('relationships'):
        print(f"Memory: {result['text']}")
        print(f"Related memories: {result['relationships']['count']}")
```

### 🛡️ Enterprise-Grade Reliability

- **Automatic Retry Logic**: Exponential backoff (1s, 2s, 4s) with 3 retry attempts
- **Rate Limiting Handling**: Automatic retry on 429 errors with respect for rate limits
- **Network Timeout Recovery**: Configurable timeouts with automatic recovery
- **Input Sanitization**: Protection against injection attacks (SQL, XSS, command injection)
- **Comprehensive Error Handling**: Detailed error messages and status codes

```python
# Configure timeout and automatic retries
rb = RecallBricks(
    api_key="rb_dev_xxx",  # or service_token="rbk_service_xxx"
    timeout=30  # 30 second timeout
)

# All methods automatically retry on transient failures
memory = rb.save("Important data")  # Retries up to 3 times on failure
```

## API Reference

### Core Methods

#### `learn(text, user_id=None, project_id=None, source="python-sdk", metadata=None, max_retries=3)`
Store a memory with automatic metadata extraction. Returns the memory with auto-generated tags, category, entities, importance, and summary. Note: `user_id` is required when using service token authentication.

#### `recall(query, limit=10, min_helpfulness_score=None, organized=False, user_id=None, project_id=None)`
Recall memories with semantic search. When `organized=True`, returns results organized by category with summaries. Note: `user_id` is required when using service token authentication.

#### `save(text, user_id=None, source="api", project_id="default", tags=None, metadata=None, max_retries=3)`
Save a new memory with automatic retry on failure. Note: `user_id` is required when using service token authentication.

#### `save_memory(...)` (DEPRECATED)
Deprecated alias for `save()`. Use `learn()` instead for automatic metadata extraction.

#### `get_all(limit=None)`
Retrieve all memories.

#### `search(query, limit=10, include_relationships=False)`
Search memories by text.

#### `get(memory_id)`
Get a specific memory by ID.

#### `delete(memory_id)`
Delete a memory.

### Metacognition Methods (Phase 2A)

#### `predict_memories(context=None, recent_memory_ids=None, limit=10)`
Predict which memories might be useful.

#### `suggest_memories(context, limit=5, min_confidence=0.6, include_reasoning=True)`
Get memory suggestions based on context.

#### `get_learning_metrics(days=30)`
Get learning metrics showing memory usage patterns.

#### `get_patterns(days=30)`
Analyze patterns in memory usage and access.

#### `search_weighted(query, limit=10, weight_by_usage=False, decay_old_memories=False, adaptive_weights=True, min_helpfulness_score=None)`
Search with intelligent weighting.

### Relationship Methods

#### `get_relationships(memory_id)`
Get relationships for a specific memory.

#### `get_graph_context(memory_id, depth=2)`
Get memory graph with relationships at specified depth.

### Autonomous Agent Clients (v1.3.0)

All autonomous clients are initialized with `api_key` and optional `base_url`:

```python
from recallbricks.autonomous import WorkingMemoryClient
client = WorkingMemoryClient(api_key="rb_dev_xxx")
```

#### WorkingMemoryClient
- `store(agent_id, content, memory_type, priority, ttl_seconds, metadata)` - Store working memory
- `retrieve(agent_id, memory_type, limit, min_priority)` - Retrieve working memories
- `update(memory_id, content, priority, metadata)` - Update a memory
- `delete(memory_id)` - Delete a memory
- `clear(agent_id, memory_type)` - Clear all working memory
- `consolidate(agent_id, strategy)` - Consolidate to long-term storage

#### ProspectiveMemoryClient
- `create(agent_id, content, trigger_type, trigger_at, trigger_condition, priority)` - Create reminder
- `get(memory_id)` - Get specific prospective memory
- `get_pending(agent_id, limit, include_triggered)` - Get pending reminders
- `check_triggers(agent_id)` - Check for triggered reminders
- `mark_completed(memory_id, outcome)` - Mark as completed
- `cancel(memory_id, reason)` - Cancel a reminder
- `reschedule(memory_id, trigger_at)` - Reschedule a reminder

#### MetacognitionClient
- `log_reasoning(agent_id, step, reasoning, confidence, alternatives)` - Log reasoning
- `evaluate_confidence(agent_id, decision, context, evidence)` - Evaluate confidence
- `get_reasoning_trace(agent_id, session_id, limit)` - Get reasoning trace
- `analyze_patterns(agent_id, days)` - Analyze patterns
- `get_biases(agent_id)` - Get detected biases
- `self_reflect(agent_id, topic, depth)` - Trigger self-reflection

#### MemoryTypesClient
- `store_episodic(agent_id, event, context, importance, emotions)` - Store event memory
- `store_semantic(agent_id, fact, category, confidence, source)` - Store fact memory
- `store_procedural(agent_id, skill, steps, proficiency)` - Store skill memory
- `retrieve(agent_id, memory_type, query, limit)` - Retrieve by type
- `get_statistics(agent_id)` - Get memory statistics
- `consolidate_semantic(agent_id, category)` - Consolidate semantic memories

#### GoalsClient
- `create(agent_id, title, description, priority, deadline, success_criteria)` - Create goal
- `get(goal_id)` - Get specific goal
- `list(agent_id, status, include_subgoals, limit)` - List goals
- `update_progress(goal_id, progress, notes)` - Update progress
- `add_subgoal(parent_goal_id, title, description)` - Add subgoal
- `complete(goal_id, outcome)` - Mark completed
- `cancel(goal_id, reason)` - Cancel goal
- `get_hierarchy(goal_id)` - Get goal tree
- `suggest_next_steps(goal_id)` - Get AI suggestions

#### HealthClient
- `check(agent_id)` - Check agent health
- `get_metrics(agent_id, period, metrics)` - Get performance metrics
- `get_memory_usage(agent_id)` - Get memory usage stats
- `get_error_log(agent_id, severity, limit)` - Get error log
- `run_diagnostics(agent_id)` - Run full diagnostics
- `get_quota_status(agent_id)` - Get quota status
- `ping()` - Simple health check
- `get_uptime(agent_id)` - Get uptime stats

#### UncertaintyClient
- `record(agent_id, topic, confidence, reasoning, factors)` - Record uncertainty
- `get_by_topic(agent_id, topic)` - Get uncertainty by topic
- `get_summary(agent_id, period)` - Get uncertainty summary
- `calibrate(agent_id, topic, actual_outcome, predicted_confidence)` - Calibrate
- `get_calibration_score(agent_id)` - Get calibration score
- `suggest_information_needs(agent_id, threshold)` - Suggest info needs
- `resolve(uncertainty_id, resolution, new_confidence)` - Resolve uncertainty

#### ContextClient
- `create_session(agent_id, context_type, initial_context, ttl_seconds)` - Create session
- `get(session_id)` - Get session context
- `update(session_id, context_data, merge)` - Update context
- `add_to_history(session_id, entry)` - Add history entry
- `get_history(session_id, limit)` - Get session history
- `list_sessions(agent_id, active_only, limit)` - List sessions
- `end_session(session_id, summary)` - End session
- `get_environment(agent_id)` - Get environment
- `set_environment(agent_id, environment)` - Set environment

#### SearchClient
- `semantic(agent_id, query, limit, min_score, memory_types)` - Semantic search
- `filtered(agent_id, query, filters, limit, sort_by)` - Filtered search
- `hybrid(agent_id, query, keyword_weight, semantic_weight, limit)` - Hybrid search
- `similar(agent_id, memory_id, limit, exclude_self)` - Find similar
- `temporal(agent_id, start_time, end_time, query, limit)` - Temporal search
- `aggregate(agent_id, group_by, query, aggregation)` - Aggregate search
- `suggest(agent_id, partial_query, limit)` - Search suggestions

## Type Definitions

The SDK includes comprehensive type definitions for all Phase 2A features:

```python
from recallbricks import (
    PredictedMemory,
    SuggestedMemory,
    LearningMetrics,
    PatternAnalysis,
    WeightedSearchResult
)
```

## Error Handling

```python
from recallbricks import (
    RecallBricks,
    RecallBricksError,
    AuthenticationError,
    RateLimitError,
    APIError
)

try:
    rb = RecallBricks(api_key="rb_dev_xxx")  # or service_token="rbk_service_xxx"
    memory = rb.save("Test memory")
except AuthenticationError:
    print("Invalid API key or service token")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}")
except APIError as e:
    print(f"API error: {e.status_code}")
except RecallBricksError as e:
    print(f"General error: {str(e)}")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python tests/test_authentication.py    # Authentication tests
python tests/test_relationships.py     # Relationship tests
python tests/test_stress.py           # Stress tests
python tests/test_load_stress.py      # Load stress tests
python tests/test_phase2a_security.py # Security tests

# Run with coverage
pip install pytest pytest-cov
pytest tests/ --cov=recallbricks --cov-report=html
```

## Migration Guide (v1.1.x to v1.2.0)

### Breaking Changes
None! v1.2.0 is fully backward compatible with v1.1.x.

### New Features

#### 1. Use `learn()` instead of `save()` for automatic metadata
```python
# Before (v1.1.x) - manual tags required
rb.save("User prefers dark mode", tags=["preference", "ui"])

# After (v1.2.0) - automatic metadata extraction
result = rb.learn("User prefers dark mode")
# result['metadata'] contains auto-generated tags, category, entities, etc.
```

#### 2. Use `recall()` with organized results
```python
# Before (v1.1.x) - basic search
results = rb.search("dark mode")

# After (v1.2.0) - organized recall with category summaries
results = rb.recall("dark mode", organized=True)
# results['categories'] contains category summaries
```

### Deprecated Methods
- `save_memory()` - Use `learn()` instead. Will show a DeprecationWarning.

### New Type Definitions
```python
from recallbricks import (
    # Phase 2B types
    MemoryMetadata,
    CategorySummary,
    RecallMemory,
    RecallResponse,
    LearnedMemory,
    OrganizedRecallResult
)
```

## Documentation

- **Full Documentation**: https://recallbricks.com/docs
- **API Reference**: https://recallbricks.com/docs/api
- **TypeScript SDK**: https://github.com/recallbricks/recallbricks-typescript

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Support

- **GitHub Issues**: https://github.com/recallbricks/recallbricks-python/issues
- **Email**: support@recallbricks.com
- **Documentation**: https://recallbricks.com/docs
