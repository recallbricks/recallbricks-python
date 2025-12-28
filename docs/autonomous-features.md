# RecallBricks Autonomous Agent Features

Build truly autonomous AI agents with specialized memory and cognition clients.

## Overview

The `recallbricks.autonomous` module provides 9 specialized clients for different aspects of autonomous agent memory and cognition:

| Client | Purpose |
|--------|---------|
| `WorkingMemoryClient` | Active, short-term memory management |
| `ProspectiveMemoryClient` | Future-oriented memory (reminders, scheduled tasks) |
| `MetacognitionClient` | Self-awareness and reasoning about cognition |
| `MemoryTypesClient` | Episodic, semantic, and procedural memory |
| `GoalsClient` | Goal setting and progress tracking |
| `HealthClient` | Agent health and performance monitoring |
| `UncertaintyClient` | Confidence calibration and uncertainty tracking |
| `ContextClient` | Session and environmental context management |
| `SearchClient` | Advanced memory search capabilities |

## Quick Start

```python
from recallbricks.autonomous import (
    WorkingMemoryClient,
    GoalsClient,
    MetacognitionClient
)

# Initialize clients
working_memory = WorkingMemoryClient(api_key="rb_dev_xxx")
goals = GoalsClient(api_key="rb_dev_xxx")
metacognition = MetacognitionClient(api_key="rb_dev_xxx")
```

---

## WorkingMemoryClient

Manages active, short-term memory for AI agents.

### Methods

#### store()

Store content in working memory.

```python
def store(
    agent_id: str,
    content: str,
    memory_type: str = "context",
    priority: float = 0.5,
    ttl_seconds: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = WorkingMemoryClient(api_key="rb_dev_xxx")

result = client.store(
    agent_id="agent_123",
    content="User is asking about authentication",
    memory_type="context",
    priority=0.8,
    ttl_seconds=3600  # 1 hour
)
```

#### retrieve()

Retrieve working memory for an agent.

```python
def retrieve(
    agent_id: str,
    memory_type: Optional[str] = None,
    limit: int = 10,
    min_priority: Optional[float] = None
) -> Dict[str, Any]
```

#### update()

Update an existing working memory entry.

```python
def update(
    memory_id: str,
    content: Optional[str] = None,
    priority: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

#### delete()

Delete a working memory entry.

```python
def delete(memory_id: str) -> Dict[str, Any]
```

#### clear()

Clear all working memory for an agent.

```python
def clear(
    agent_id: str,
    memory_type: Optional[str] = None
) -> Dict[str, Any]
```

#### consolidate()

Consolidate working memory to long-term storage.

```python
def consolidate(
    agent_id: str,
    strategy: str = "importance"  # importance, recency, relevance
) -> Dict[str, Any]
```

---

## ProspectiveMemoryClient

Manages future-oriented memory for scheduled tasks and reminders.

### Methods

#### create()

Create a prospective memory (scheduled task/reminder).

```python
def create(
    agent_id: str,
    content: str,
    trigger_type: str = "time",  # time, event, condition
    trigger_at: Optional[str] = None,
    trigger_condition: Optional[str] = None,
    priority: float = 0.5,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = ProspectiveMemoryClient(api_key="rb_dev_xxx")

# Time-based reminder
reminder = client.create(
    agent_id="agent_123",
    content="Follow up with user about API integration",
    trigger_type="time",
    trigger_at="2024-12-28T10:00:00Z"
)

# Event-based trigger
client.create(
    agent_id="agent_123",
    content="Notify user when deployment completes",
    trigger_type="event",
    trigger_condition="deployment.status == 'completed'"
)
```

#### get_pending()

Get pending prospective memories.

```python
def get_pending(
    agent_id: str,
    limit: int = 10,
    include_triggered: bool = False
) -> Dict[str, Any]
```

#### check_triggers()

Check for triggered reminders.

```python
def check_triggers(agent_id: str) -> Dict[str, Any]
```

#### mark_completed()

Mark as completed.

```python
def mark_completed(
    memory_id: str,
    outcome: Optional[str] = None
) -> Dict[str, Any]
```

#### cancel()

Cancel a reminder.

```python
def cancel(
    memory_id: str,
    reason: Optional[str] = None
) -> Dict[str, Any]
```

#### reschedule()

Reschedule a reminder.

```python
def reschedule(
    memory_id: str,
    trigger_at: str
) -> Dict[str, Any]
```

---

## MetacognitionClient

Enables agent self-awareness and reasoning about cognitive processes.

### Methods

#### log_reasoning()

Log a reasoning step for metacognitive tracking.

```python
def log_reasoning(
    agent_id: str,
    step: str,
    reasoning: str,
    confidence: float = 0.5,
    alternatives: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = MetacognitionClient(api_key="rb_dev_xxx")

client.log_reasoning(
    agent_id="agent_123",
    step="solution_selection",
    reasoning="Chose JWT over OAuth for simplicity",
    confidence=0.8,
    alternatives=["OAuth 2.0", "API Keys"]
)
```

#### evaluate_confidence()

Evaluate confidence in a decision.

```python
def evaluate_confidence(
    agent_id: str,
    decision: str,
    context: Optional[str] = None,
    evidence: Optional[List[str]] = None
) -> Dict[str, Any]
```

#### get_reasoning_trace()

Get the reasoning trace for an agent.

```python
def get_reasoning_trace(
    agent_id: str,
    session_id: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]
```

#### analyze_patterns()

Analyze metacognitive patterns over time.

```python
def analyze_patterns(
    agent_id: str,
    days: int = 7
) -> Dict[str, Any]
```

#### get_biases()

Get detected cognitive biases.

```python
def get_biases(agent_id: str) -> Dict[str, Any]
```

#### self_reflect()

Trigger agent self-reflection.

```python
def self_reflect(
    agent_id: str,
    topic: str,
    depth: str = "standard"  # brief, standard, deep
) -> Dict[str, Any]
```

---

## MemoryTypesClient

Manages different types of memory: episodic, semantic, and procedural.

### Methods

#### store_episodic()

Store an episodic memory (event/experience).

```python
def store_episodic(
    agent_id: str,
    event: str,
    context: Optional[Dict[str, Any]] = None,
    importance: float = 0.5,
    emotions: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = MemoryTypesClient(api_key="rb_dev_xxx")

client.store_episodic(
    agent_id="agent_123",
    event="Successfully debugged authentication issue",
    context={"project": "api-server", "duration": "2 hours"},
    importance=0.8,
    emotions=["satisfaction", "relief"]
)
```

#### store_semantic()

Store a semantic memory (fact/knowledge).

```python
def store_semantic(
    agent_id: str,
    fact: str,
    category: Optional[str] = None,
    confidence: float = 0.8,
    source: Optional[str] = None,
    related_concepts: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

#### store_procedural()

Store a procedural memory (skill/how-to).

```python
def store_procedural(
    agent_id: str,
    skill: str,
    steps: List[str],
    proficiency: float = 0.5,
    prerequisites: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

#### retrieve()

Retrieve memories by type.

```python
def retrieve(
    agent_id: str,
    memory_type: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 10
) -> Dict[str, Any]
```

#### get_statistics()

Get memory type statistics.

```python
def get_statistics(agent_id: str) -> Dict[str, Any]
```

---

## GoalsClient

Manages agent goals and objectives with hierarchical support.

### Methods

#### create()

Create a new goal.

```python
def create(
    agent_id: str,
    title: str,
    description: Optional[str] = None,
    priority: float = 0.5,
    deadline: Optional[str] = None,
    parent_goal_id: Optional[str] = None,
    success_criteria: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = GoalsClient(api_key="rb_dev_xxx")

goal = client.create(
    agent_id="agent_123",
    title="Implement OAuth integration",
    priority=0.9,
    success_criteria=[
        "Login flow works",
        "Token refresh implemented",
        "All tests passing"
    ]
)
```

#### list()

List goals for an agent.

```python
def list(
    agent_id: str,
    status: Optional[str] = None,  # active, completed, cancelled
    include_subgoals: bool = True,
    limit: int = 20
) -> Dict[str, Any]
```

#### update_progress()

Update goal progress.

```python
def update_progress(
    goal_id: str,
    progress: float,  # 0-100
    notes: Optional[str] = None
) -> Dict[str, Any]
```

#### add_subgoal()

Add a subgoal.

```python
def add_subgoal(
    parent_goal_id: str,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]
```

#### complete()

Mark as completed.

```python
def complete(
    goal_id: str,
    outcome: Optional[str] = None
) -> Dict[str, Any]
```

#### cancel()

Cancel a goal.

```python
def cancel(
    goal_id: str,
    reason: Optional[str] = None
) -> Dict[str, Any]
```

#### get_hierarchy()

Get the full goal hierarchy.

```python
def get_hierarchy(goal_id: str) -> Dict[str, Any]
```

#### suggest_next_steps()

Get AI-suggested next steps.

```python
def suggest_next_steps(goal_id: str) -> Dict[str, Any]
```

---

## HealthClient

Monitors agent health and performance.

### Methods

#### check()

Check overall health status.

```python
def check(agent_id: str) -> Dict[str, Any]
```

#### get_metrics()

Get performance metrics.

```python
def get_metrics(
    agent_id: str,
    period: str = "1h",  # 1h, 24h, 7d, 30d
    metrics: Optional[List[str]] = None
) -> Dict[str, Any]
```

#### get_memory_usage()

Get memory usage statistics.

```python
def get_memory_usage(agent_id: str) -> Dict[str, Any]
```

#### get_error_log()

Get error log.

```python
def get_error_log(
    agent_id: str,
    severity: Optional[str] = None,  # error, warning, info
    limit: int = 50
) -> Dict[str, Any]
```

#### run_diagnostics()

Run full diagnostics.

```python
def run_diagnostics(agent_id: str) -> Dict[str, Any]
```

#### ping()

Simple health check for the API.

```python
def ping() -> Dict[str, Any]
```

---

## UncertaintyClient

Manages uncertainty quantification and confidence calibration.

### Methods

#### record()

Record an uncertainty measurement.

```python
def record(
    agent_id: str,
    topic: str,
    confidence: float,
    reasoning: Optional[str] = None,
    factors: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Example:**

```python
client = UncertaintyClient(api_key="rb_dev_xxx")

client.record(
    agent_id="agent_123",
    topic="Database selection",
    confidence=0.6,
    reasoning="PostgreSQL is proven but MongoDB might scale better",
    factors=[
        {"name": "experience", "impact": 0.3},
        {"name": "research", "impact": 0.2}
    ]
)
```

#### calibrate()

Calibrate based on actual outcome.

```python
def calibrate(
    agent_id: str,
    topic: str,
    actual_outcome: str,
    predicted_confidence: float
) -> Dict[str, Any]
```

#### get_calibration_score()

Get calibration score.

```python
def get_calibration_score(agent_id: str) -> Dict[str, Any]
```

#### suggest_information_needs()

Suggest areas needing more information.

```python
def suggest_information_needs(
    agent_id: str,
    threshold: float = 0.5
) -> Dict[str, Any]
```

---

## ContextClient

Manages session and environmental context.

### Methods

#### create_session()

Create a new context session.

```python
def create_session(
    agent_id: str,
    context_type: str = "conversation",  # conversation, task, workflow
    initial_context: Optional[Dict[str, Any]] = None,
    ttl_seconds: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

#### update()

Update session context.

```python
def update(
    session_id: str,
    context_data: Dict[str, Any],
    merge: bool = True
) -> Dict[str, Any]
```

#### add_to_history()

Add an entry to session history.

```python
def add_to_history(
    session_id: str,
    entry: Dict[str, Any]
) -> Dict[str, Any]
```

#### end_session()

End a session.

```python
def end_session(
    session_id: str,
    summary: Optional[str] = None
) -> Dict[str, Any]
```

#### set_environment()

Set agent environment.

```python
def set_environment(
    agent_id: str,
    environment: Dict[str, Any]
) -> Dict[str, Any]
```

---

## SearchClient

Advanced memory search capabilities.

### Methods

#### semantic()

Semantic search across memories.

```python
def semantic(
    agent_id: str,
    query: str,
    limit: int = 10,
    min_score: float = 0.0,
    memory_types: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

#### hybrid()

Hybrid search (keyword + semantic).

```python
def hybrid(
    agent_id: str,
    query: str,
    keyword_weight: float = 0.3,
    semantic_weight: float = 0.7,
    limit: int = 10
) -> Dict[str, Any]
```

#### similar()

Find similar memories.

```python
def similar(
    agent_id: str,
    memory_id: str,
    limit: int = 10,
    exclude_self: bool = True
) -> Dict[str, Any]
```

#### temporal()

Search within a time range.

```python
def temporal(
    agent_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]
```

#### aggregate()

Aggregate memories by field.

```python
def aggregate(
    agent_id: str,
    group_by: str,
    query: Optional[str] = None,
    aggregation: str = "count"
) -> Dict[str, Any]
```

#### suggest()

Get search suggestions.

```python
def suggest(
    agent_id: str,
    partial_query: str,
    limit: int = 5
) -> Dict[str, Any]
```
