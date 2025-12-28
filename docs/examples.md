# RecallBricks Python SDK - Examples

Working code examples for common use cases. All examples are copy-paste runnable.

## Table of Contents

- [Basic Memory Operations](#basic-memory-operations)
- [Working Memory Session](#working-memory-session)
- [Goal Tracking](#goal-tracking)
- [Metacognition Assessment](#metacognition-assessment)
- [Memory Types](#memory-types)
- [Search Operations](#search-operations)
- [Error Handling](#error-handling)
- [Decorator Usage](#decorator-usage)

---

## Basic Memory Operations

### Save and Recall Memories

```python
from recallbricks import RecallBricks

# Initialize client
rb = RecallBricks(api_key="rb_dev_your_api_key")

# Save a memory with tags
memory = rb.save(
    text="User prefers dark mode and TypeScript for frontend development",
    tags=["preference", "ui", "typescript"],
    metadata={"source": "onboarding"}
)
print(f"Saved memory ID: {memory['id']}")

# Learn with automatic metadata extraction
learned = rb.learn("Fixed critical authentication bug using JWT refresh tokens")
print(f"Auto-generated tags: {learned['metadata']['tags']}")
print(f"Category: {learned['metadata']['category']}")
print(f"Importance: {learned['metadata']['importance']}")

# Recall memories with semantic search
results = rb.recall("authentication issues", limit=5)
print(f"\nFound {results['count']} relevant memories:")
for mem in results['memories']:
    print(f"  - {mem['text'][:80]}...")

# Organized recall with categories
organized = rb.recall("user preferences", organized=True)
for category, info in organized.get('categories', {}).items():
    print(f"\n{category} ({info['count']} memories):")
    print(f"  Summary: {info['summary']}")
```

### Update and Delete Memories

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")

# Create a memory
memory = rb.save("Initial content about the project")
memory_id = memory['id']

# Update the memory
updated = rb.update(
    memory_id=memory_id,
    text="Updated content with more details",
    tags=["updated", "project"],
    metadata={"version": 2}
)
print(f"Updated at: {updated.get('updated_at')}")

# Get specific memory
fetched = rb.get(memory_id)
print(f"Current text: {fetched['text']}")

# Delete the memory
result = rb.delete(memory_id)
print(f"Deleted: {result}")
```

---

## Working Memory Session

### Managing Short-Term Context

```python
from recallbricks.autonomous import WorkingMemoryClient

client = WorkingMemoryClient(api_key="rb_dev_xxx")
agent_id = "agent_customer_support_001"

# Store conversation context
client.store(
    agent_id=agent_id,
    content="Customer is asking about refund policy",
    memory_type="context",
    priority=0.9
)

client.store(
    agent_id=agent_id,
    content="Customer has order #12345 from last week",
    memory_type="context",
    priority=0.8
)

client.store(
    agent_id=agent_id,
    content="Customer seems frustrated - use empathetic tone",
    memory_type="observation",
    priority=0.7
)

# Retrieve all working memories
memories = client.retrieve(agent_id=agent_id, limit=10)
print(f"Active working memories: {len(memories['memories'])}")
for mem in memories['memories']:
    print(f"  [{mem['memory_type']}] {mem['content']}")

# Retrieve high-priority only
high_priority = client.retrieve(
    agent_id=agent_id,
    min_priority=0.8
)
print(f"\nHigh priority memories: {len(high_priority['memories'])}")

# Consolidate to long-term storage
result = client.consolidate(agent_id=agent_id, strategy="importance")
print(f"\nConsolidated {result.get('consolidated_count', 0)} memories to long-term storage")

# Clear working memory after conversation ends
cleared = client.clear(agent_id=agent_id)
print(f"Cleared {cleared.get('deleted_count', 0)} working memories")
```

---

## Goal Tracking

### Hierarchical Goal Management

```python
from recallbricks.autonomous import GoalsClient

client = GoalsClient(api_key="rb_dev_xxx")
agent_id = "agent_developer_001"

# Create a main goal
main_goal = client.create(
    agent_id=agent_id,
    title="Implement User Authentication System",
    description="Build secure authentication with OAuth and JWT",
    priority=0.9,
    success_criteria=[
        "Login endpoint functional",
        "OAuth providers integrated",
        "JWT tokens properly validated",
        "Refresh token mechanism working",
        "All security tests passing"
    ]
)
goal_id = main_goal['id']
print(f"Created goal: {main_goal['title']}")

# Add subgoals
subgoal1 = client.add_subgoal(
    parent_goal_id=goal_id,
    title="Research OAuth Providers",
    description="Compare Google, GitHub, and Microsoft OAuth implementations"
)

subgoal2 = client.add_subgoal(
    parent_goal_id=goal_id,
    title="Implement JWT Token System"
)

subgoal3 = client.add_subgoal(
    parent_goal_id=goal_id,
    title="Write Integration Tests"
)

# Update progress
client.update_progress(
    goal_id=subgoal1['id'],
    progress=100,
    notes="Completed research, chose Google and GitHub OAuth"
)

client.update_progress(
    goal_id=goal_id,
    progress=25,
    notes="Research phase complete, starting implementation"
)

# Complete a subgoal
client.complete(
    goal_id=subgoal1['id'],
    outcome="Selected Google and GitHub as OAuth providers"
)

# Get AI suggestions for next steps
suggestions = client.suggest_next_steps(goal_id=goal_id)
print("\nAI-suggested next steps:")
for step in suggestions.get('steps', []):
    print(f"  - {step.get('action')}: {step.get('reasoning')}")

# View goal hierarchy
hierarchy = client.get_hierarchy(goal_id=goal_id)
print(f"\nGoal Hierarchy:")
print(f"  {hierarchy['title']} ({hierarchy.get('progress', 0)}%)")
for sub in hierarchy.get('subgoals', []):
    status = "Done" if sub.get('status') == 'completed' else f"{sub.get('progress', 0)}%"
    print(f"    - {sub['title']} [{status}]")

# List all active goals
active_goals = client.list(agent_id=agent_id, status="active")
print(f"\nActive goals: {len(active_goals.get('goals', []))}")
```

---

## Metacognition Assessment

### Self-Awareness and Reasoning Tracking

```python
from recallbricks.autonomous import MetacognitionClient

client = MetacognitionClient(api_key="rb_dev_xxx")
agent_id = "agent_architect_001"

# Log reasoning steps during decision-making
client.log_reasoning(
    agent_id=agent_id,
    step="problem_analysis",
    reasoning="User needs real-time updates. Considering WebSockets vs SSE vs polling.",
    confidence=0.9
)

client.log_reasoning(
    agent_id=agent_id,
    step="option_evaluation",
    reasoning="WebSockets: bi-directional, complex. SSE: simpler, one-way. Polling: fallback option.",
    confidence=0.85,
    alternatives=["WebSockets", "Server-Sent Events", "Long Polling"]
)

client.log_reasoning(
    agent_id=agent_id,
    step="decision",
    reasoning="Chose SSE for simplicity - only need server-to-client updates",
    confidence=0.8,
    metadata={"selected": "SSE", "reasoning_time_ms": 1500}
)

# Evaluate confidence in the decision
evaluation = client.evaluate_confidence(
    agent_id=agent_id,
    decision="Use Server-Sent Events for real-time updates",
    context="Building a notification system for a medium-traffic web app",
    evidence=[
        "SSE is simpler to implement",
        "Only server-to-client communication needed",
        "Good browser support",
        "Team has experience with SSE"
    ]
)
print(f"Decision confidence: {evaluation.get('confidence')}")
print(f"Assessment: {evaluation.get('assessment')}")

# Get reasoning trace
trace = client.get_reasoning_trace(agent_id=agent_id, limit=10)
print("\nReasoning Trace:")
for entry in trace.get('entries', []):
    print(f"  [{entry['step']}] {entry['reasoning'][:60]}...")

# Analyze patterns in decision-making
patterns = client.analyze_patterns(agent_id=agent_id, days=30)
print(f"\nPattern Analysis:")
print(f"  Average confidence: {patterns.get('avg_confidence')}")
print(f"  Decision patterns: {patterns.get('patterns')}")

# Check for cognitive biases
biases = client.get_biases(agent_id=agent_id)
print("\nDetected Biases:")
for bias in biases.get('detected', []):
    print(f"  {bias['type']}: {bias['description']}")
    print(f"    Mitigation: {bias['mitigation']}")

# Self-reflect on recent decisions
reflection = client.self_reflect(
    agent_id=agent_id,
    topic="Architecture decisions this week",
    depth="deep"
)
print(f"\nSelf-Reflection Insights:")
print(f"  {reflection.get('insights')}")
```

---

## Memory Types

### Episodic, Semantic, and Procedural Memories

```python
from recallbricks.autonomous import MemoryTypesClient

client = MemoryTypesClient(api_key="rb_dev_xxx")
agent_id = "agent_learner_001"

# Store episodic memory (event/experience)
client.store_episodic(
    agent_id=agent_id,
    event="Successfully resolved production outage caused by memory leak",
    context={
        "project": "api-gateway",
        "duration": "3 hours",
        "impact": "high",
        "root_cause": "unbounded cache"
    },
    importance=0.95,
    emotions=["relief", "accomplishment", "fatigue"]
)

# Store semantic memory (fact/knowledge)
client.store_semantic(
    agent_id=agent_id,
    fact="Redis EXPIRE command sets a timeout on a key after which the key is deleted",
    category="databases",
    confidence=0.99,
    source="Redis documentation",
    related_concepts=["caching", "TTL", "key-value stores"]
)

client.store_semantic(
    agent_id=agent_id,
    fact="Memory leaks in Node.js often occur due to unbounded event listeners or global variables",
    category="debugging",
    confidence=0.9,
    source="Production incident analysis"
)

# Store procedural memory (skill/how-to)
client.store_procedural(
    agent_id=agent_id,
    skill="Debug Memory Leak in Node.js",
    steps=[
        "Take heap snapshot using Chrome DevTools or node --inspect",
        "Compare snapshots over time to identify growing objects",
        "Check for event listener accumulation",
        "Review global variable usage",
        "Use memory profiling tools like clinic.js",
        "Implement fix and verify with load testing"
    ],
    proficiency=0.85,
    prerequisites=["Node.js experience", "Chrome DevTools knowledge"]
)

# Retrieve memories by type
semantic_memories = client.retrieve(
    agent_id=agent_id,
    memory_type="semantic",
    query="memory management"
)
print(f"Related semantic memories: {len(semantic_memories.get('memories', []))}")

# Get statistics
stats = client.get_statistics(agent_id=agent_id)
print("\nMemory Statistics:")
print(f"  Episodic: {stats.get('episodic', {}).get('count', 0)}")
print(f"  Semantic: {stats.get('semantic', {}).get('count', 0)}")
print(f"  Procedural: {stats.get('procedural', {}).get('count', 0)}")
```

---

## Search Operations

### Advanced Search Capabilities

```python
from recallbricks.autonomous import SearchClient

client = SearchClient(api_key="rb_dev_xxx")
agent_id = "agent_search_001"

# Semantic search
results = client.semantic(
    agent_id=agent_id,
    query="authentication security best practices",
    limit=10,
    min_score=0.7
)
print(f"Semantic search results: {len(results.get('results', []))}")
for r in results.get('results', [])[:3]:
    print(f"  [{r['score']:.2f}] {r['content'][:60]}...")

# Hybrid search (keyword + semantic)
hybrid_results = client.hybrid(
    agent_id=agent_id,
    query="JWT token refresh",
    keyword_weight=0.4,
    semantic_weight=0.6,
    limit=5
)
print(f"\nHybrid search results: {len(hybrid_results.get('results', []))}")

# Find similar memories
if results.get('results'):
    similar = client.similar(
        agent_id=agent_id,
        memory_id=results['results'][0]['id'],
        limit=5
    )
    print(f"\nSimilar to first result: {len(similar.get('results', []))}")

# Temporal search (time-based)
temporal_results = client.temporal(
    agent_id=agent_id,
    start_time="2024-12-01T00:00:00Z",
    end_time="2024-12-31T23:59:59Z",
    query="security",
    limit=20
)
print(f"\nMemories from December 2024: {len(temporal_results.get('results', []))}")

# Aggregate by category
aggregation = client.aggregate(
    agent_id=agent_id,
    group_by="category",
    aggregation="count"
)
print("\nMemories by category:")
for bucket in aggregation.get('buckets', []):
    print(f"  {bucket['key']}: {bucket['count']}")

# Search suggestions
suggestions = client.suggest(
    agent_id=agent_id,
    partial_query="auth",
    limit=5
)
print(f"\nSearch suggestions for 'auth': {suggestions.get('suggestions', [])}")
```

---

## Error Handling

### Comprehensive Error Handling

```python
from recallbricks import (
    RecallBricks,
    RecallBricksError,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError,
    NotFoundError
)
import time

def safe_memory_operation():
    try:
        rb = RecallBricks(api_key="rb_dev_xxx")

        # Attempt to save memory
        result = rb.save("Important information")
        print(f"Saved: {result['id']}")

        # Attempt to get a memory
        memory = rb.get("nonexistent-id")

    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
        print(f"Hint: {e.hint}")
        # Handle: Check API key, refresh credentials

    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
        print(f"Retry after: {e.retry_after} seconds")
        # Handle: Wait and retry
        time.sleep(int(e.retry_after or 60))

    except NotFoundError as e:
        print(f"Not found: {e.message}")
        print(f"Request ID: {e.request_id}")
        # Handle: Check if resource exists

    except ValidationError as e:
        print(f"Validation failed: {e.message}")
        print(f"Field: {e.field}")
        # Handle: Fix input data

    except APIError as e:
        print(f"API error ({e.status_code}): {e.message}")
        print(f"Error code: {e.code}")
        # Handle: Log and retry or escalate

    except RecallBricksError as e:
        print(f"General SDK error: {e.message}")
        print(f"Code: {e.code}")
        # Handle: Log and investigate

# Run the example
safe_memory_operation()
```

---

## Decorator Usage

### Automatic Function Capture

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")

# Decorator to capture function inputs and outputs
@rb.capture_function(save_inputs=True, save_outputs=True, include_errors=True)
def process_customer_request(customer_id: str, request_type: str):
    """Process a customer support request."""
    # Simulate processing
    if request_type == "refund":
        return {"status": "approved", "amount": 99.99}
    elif request_type == "inquiry":
        return {"status": "resolved", "response": "FAQ link sent"}
    else:
        raise ValueError(f"Unknown request type: {request_type}")

# These function calls are automatically saved to memory
try:
    result1 = process_customer_request("cust_123", "refund")
    print(f"Refund result: {result1}")

    result2 = process_customer_request("cust_456", "inquiry")
    print(f"Inquiry result: {result2}")

    # This will trigger an error capture
    result3 = process_customer_request("cust_789", "unknown")
except ValueError as e:
    print(f"Error captured: {e}")

# Check saved memories
memories = rb.search("AUTO-CAPTURE", limit=10)
print(f"\nCaptured function calls: {memories['count']}")
for mem in memories['memories']:
    print(f"  - {mem['text'][:80]}...")
```

---

## Complete Agent Example

### Building an Autonomous Agent

```python
from recallbricks import RecallBricks
from recallbricks.autonomous import (
    WorkingMemoryClient,
    GoalsClient,
    MetacognitionClient,
    ContextClient
)

class AutonomousAgent:
    def __init__(self, api_key: str, agent_id: str):
        self.agent_id = agent_id
        self.rb = RecallBricks(api_key=api_key)
        self.working_memory = WorkingMemoryClient(api_key=api_key)
        self.goals = GoalsClient(api_key=api_key)
        self.metacognition = MetacognitionClient(api_key=api_key)
        self.context = ContextClient(api_key=api_key)
        self.session = None

    def start_session(self, context_type: str = "task"):
        """Start a new context session."""
        self.session = self.context.create_session(
            agent_id=self.agent_id,
            context_type=context_type
        )
        return self.session['id']

    def remember(self, content: str, priority: float = 0.5):
        """Store in working memory."""
        return self.working_memory.store(
            agent_id=self.agent_id,
            content=content,
            priority=priority
        )

    def learn_permanently(self, text: str):
        """Learn and store in long-term memory."""
        return self.rb.learn(text)

    def set_goal(self, title: str, criteria: list):
        """Set a new goal."""
        return self.goals.create(
            agent_id=self.agent_id,
            title=title,
            success_criteria=criteria
        )

    def log_decision(self, step: str, reasoning: str, confidence: float):
        """Log reasoning for transparency."""
        return self.metacognition.log_reasoning(
            agent_id=self.agent_id,
            step=step,
            reasoning=reasoning,
            confidence=confidence
        )

    def recall_relevant(self, query: str, limit: int = 5):
        """Recall relevant memories."""
        return self.rb.recall(query, limit=limit, organized=True)

    def end_session(self, summary: str):
        """End the current session."""
        if self.session:
            # Consolidate working memory
            self.working_memory.consolidate(
                agent_id=self.agent_id,
                strategy="importance"
            )
            # End context session
            self.context.end_session(
                session_id=self.session['id'],
                summary=summary
            )
            self.session = None

# Usage
agent = AutonomousAgent(
    api_key="rb_dev_xxx",
    agent_id="agent_autonomous_001"
)

# Start working on a task
session_id = agent.start_session("task")
print(f"Started session: {session_id}")

# Remember context
agent.remember("User wants to build an e-commerce checkout", priority=0.9)
agent.remember("Payment integration required", priority=0.8)

# Set a goal
goal = agent.set_goal(
    title="Implement Checkout Flow",
    criteria=["Cart validation", "Payment processing", "Order confirmation"]
)

# Log reasoning
agent.log_decision(
    step="architecture",
    reasoning="Using Stripe for payments due to good documentation and security",
    confidence=0.85
)

# Learn something permanently
agent.learn_permanently("Stripe webhooks require signature verification for security")

# Recall relevant knowledge
memories = agent.recall_relevant("payment security")
print(f"Recalled {memories['count']} relevant memories")

# End session
agent.end_session("Completed checkout flow implementation planning")
print("Session ended")
```
