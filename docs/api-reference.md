# RecallBricks Python SDK - API Reference

Complete API reference for RecallBricks Python SDK v1.5.1.

## Table of Contents

- [RecallBricks Client](#recallbricks-client)
- [Core Methods](#core-methods)
- [Metacognition Methods](#metacognition-methods)
- [Relationship Methods](#relationship-methods)
- [Exceptions](#exceptions)
- [Type Definitions](#type-definitions)

---

## RecallBricks Client

### Constructor

```python
class RecallBricks:
    def __init__(
        self,
        api_key: Optional[str] = None,
        service_token: Optional[str] = None,
        base_url: str = "https://api.recallbricks.com/api/v1",
        timeout: int = 30
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `None` | RecallBricks API key for user-level access |
| `service_token` | `str` | `None` | Service token for server-to-server access |
| `base_url` | `str` | Production URL | API base URL |
| `timeout` | `int` | `30` | Request timeout in seconds |

**Note:** You must provide either `api_key` or `service_token`, but not both.

**Example:**

```python
from recallbricks import RecallBricks

# With API key
rb = RecallBricks(api_key="rb_dev_xxx")

# With service token
rb = RecallBricks(service_token="rbk_service_xxx")

# With custom settings
rb = RecallBricks(
    api_key="rb_dev_xxx",
    timeout=60
)
```

---

## Core Methods

### save()

Save a new memory with optional tags and metadata.

```python
def save(
    self,
    text: str,
    user_id: Optional[str] = None,
    source: str = "api",
    project_id: str = "default",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    max_retries: int = 3
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | required | Memory content to save |
| `user_id` | `str` | `None` | User ID (required with service token) |
| `source` | `str` | `"api"` | Source identifier |
| `project_id` | `str` | `"default"` | Project identifier |
| `tags` | `List[str]` | `None` | Optional tags |
| `metadata` | `Dict` | `None` | Optional metadata |
| `max_retries` | `int` | `3` | Max retry attempts |

**Returns:** `Dict` containing the created memory with `id`, `created_at`, etc.

**Example:**

```python
result = rb.save(
    "User prefers dark mode",
    tags=["preference", "ui"],
    metadata={"priority": "high"}
)
print(f"Saved: {result['id']}")
```

---

### learn()

Store a memory with automatic metadata extraction (tags, categories, entities, importance, summary).

```python
def learn(
    self,
    text: str,
    user_id: Optional[str] = None,
    project_id: Optional[str] = None,
    source: str = "python-sdk",
    metadata: Optional[Dict[str, Any]] = None,
    max_retries: int = 3
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | required | Memory content |
| `user_id` | `str` | `None` | User ID (required with service token) |
| `project_id` | `str` | `None` | Project identifier |
| `source` | `str` | `"python-sdk"` | Source identifier |
| `metadata` | `Dict` | `None` | Optional metadata overrides |
| `max_retries` | `int` | `3` | Max retry attempts |

**Returns:** `Dict` containing memory with auto-generated metadata:

```python
{
    "id": "uuid",
    "text": "Memory content",
    "metadata": {
        "tags": ["auto", "generated", "tags"],
        "category": "Work",
        "entities": ["Python", "RecallBricks"],
        "importance": 0.85,
        "summary": "AI-generated summary"
    },
    "created_at": "timestamp"
}
```

**Example:**

```python
result = rb.learn("Fixed authentication bug using JWT refresh tokens")
print(f"Auto-tags: {result['metadata']['tags']}")
print(f"Category: {result['metadata']['category']}")
```

---

### recall()

Recall memories with semantic search and optional organization.

```python
def recall(
    self,
    query: str,
    limit: int = 10,
    min_helpfulness_score: Optional[float] = None,
    organized: bool = False,
    user_id: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `10` | Max results |
| `min_helpfulness_score` | `float` | `None` | Filter by helpfulness (0.0-1.0) |
| `organized` | `bool` | `False` | Return organized by category |
| `user_id` | `str` | `None` | User ID filter |
| `project_id` | `str` | `None` | Project ID filter |

**Returns:**

When `organized=False`:
```python
{"memories": [...], "count": 10}
```

When `organized=True`:
```python
{
    "memories": [...],
    "categories": {
        "Work": {"count": 5, "avg_score": 0.85, "summary": "..."}
    },
    "total": 7
}
```

**Example:**

```python
# Basic recall
results = rb.recall("authentication", limit=5)

# Organized recall
results = rb.recall("preferences", organized=True, min_helpfulness_score=0.7)
for category, info in results['categories'].items():
    print(f"{category}: {info['count']} memories")
```

---

### search()

Search memories by semantic similarity.

```python
def search(
    self,
    query: str,
    limit: int = 10
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `10` | Max results |

**Returns:** `Dict` with `memories` list and `count`

---

### get_all()

Retrieve all memories.

```python
def get_all(
    self,
    limit: Optional[int] = None
) -> Dict[str, Any]
```

---

### get()

Get a specific memory by ID.

```python
def get(
    self,
    memory_id: str
) -> Dict[str, Any]
```

---

### update()

Update an existing memory.

```python
def update(
    self,
    memory_id: str,
    text: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

---

### delete()

Delete a memory.

```python
def delete(
    self,
    memory_id: str
) -> Dict[str, Any]
```

---

### health()

Check API health status.

```python
def health(self) -> Dict[str, Any]
```

---

### get_rate_limit()

Get current rate limit status.

```python
def get_rate_limit(self) -> Dict[str, Any]
```

**Returns:**

```python
{
    "limit": 1000,
    "remaining": 950,
    "reset": 1703721600,
    "percentUsed": 5.0
}
```

---

## Metacognition Methods

### predict_memories()

Predict which memories might be useful based on context.

```python
def predict_memories(
    self,
    context: Optional[str] = None,
    recent_memory_ids: Optional[List[str]] = None,
    limit: int = 10
) -> List[PredictedMemory]
```

**Returns:** List of `PredictedMemory` objects with `id`, `content`, `confidence_score`, `reasoning`

---

### suggest_memories()

Get memory suggestions based on current context.

```python
def suggest_memories(
    self,
    context: str,
    limit: int = 5,
    min_confidence: float = 0.6,
    include_reasoning: bool = True
) -> List[SuggestedMemory]
```

**Returns:** List of `SuggestedMemory` objects with `id`, `content`, `confidence`, `reasoning`, `relevance_context`

---

### get_learning_metrics()

Get learning metrics showing memory usage patterns.

```python
def get_learning_metrics(
    self,
    days: int = 30
) -> LearningMetrics
```

**Returns:** `LearningMetrics` dataclass:

```python
@dataclass
class LearningMetrics:
    avg_helpfulness: float
    total_usage: int
    active_memories: int
    total_memories: int
    trends: LearningTrends
```

---

### get_patterns()

Analyze patterns in memory usage.

```python
def get_patterns(
    self,
    days: int = 30
) -> PatternAnalysis
```

**Returns:** `PatternAnalysis` dataclass with `summary`, `most_useful_tags`, `frequently_accessed_together`, `underutilized_memories`

---

### search_weighted()

Search with intelligent weighting.

```python
def search_weighted(
    self,
    query: str,
    limit: int = 10,
    weight_by_usage: bool = False,
    decay_old_memories: bool = False,
    adaptive_weights: bool = True,
    min_helpfulness_score: Optional[float] = None
) -> List[WeightedSearchResult]
```

**Returns:** List of `WeightedSearchResult` with `relevance_score`, `usage_boost`, `helpfulness_boost`, `recency_boost`

---

## Relationship Methods

### get_relationships()

Get relationships for a specific memory.

```python
def get_relationships(
    self,
    memory_id: str
) -> Dict[str, Any]
```

---

### get_graph_context()

Get memory graph with relationships at specified depth.

```python
def get_graph_context(
    self,
    memory_id: str,
    depth: int = 2
) -> Dict[str, Any]
```

---

## Decorator

### capture_function()

Decorator that automatically captures function inputs and outputs.

```python
@rb.capture_function(
    save_inputs=True,
    save_outputs=True,
    include_errors=True
)
def my_function(arg1, arg2):
    return result
```

---

## Exceptions

### RecallBricksError

Base exception for all SDK errors.

```python
class RecallBricksError(Exception):
    message: str
    code: Optional[str]
    hint: Optional[str]
    request_id: Optional[str]
```

### AuthenticationError

Raised when API key is invalid or missing.

### RateLimitError

Raised when rate limit is exceeded.

```python
class RateLimitError(RecallBricksError):
    retry_after: Optional[str]
```

### APIError

Raised when API returns an error.

```python
class APIError(RecallBricksError):
    status_code: Optional[int]
```

### ValidationError

Raised when input validation fails.

```python
class ValidationError(RecallBricksError):
    field: Optional[str]
```

### NotFoundError

Raised when a resource is not found (404).

---

## Type Definitions

### PredictedMemory

```python
@dataclass
class PredictedMemory:
    id: str
    content: str
    confidence_score: float
    reasoning: str
    metadata: Optional[Dict[str, Any]]
```

### SuggestedMemory

```python
@dataclass
class SuggestedMemory:
    id: str
    content: str
    confidence: float
    reasoning: str
    relevance_context: str
```

### LearningMetrics

```python
@dataclass
class LearningMetrics:
    avg_helpfulness: float
    total_usage: int
    active_memories: int
    total_memories: int
    trends: LearningTrends
```

### LearningTrends

```python
@dataclass
class LearningTrends:
    helpfulness_trend: str  # 'stable', 'increasing', 'decreasing'
    usage_trend: str
    growth_rate: float
```

### PatternAnalysis

```python
@dataclass
class PatternAnalysis:
    summary: str
    most_useful_tags: List[str]
    frequently_accessed_together: List[List[str]]
    underutilized_memories: List[Dict[str, Any]]
```

### WeightedSearchResult

```python
@dataclass
class WeightedSearchResult:
    id: str
    text: str
    source: str
    project_id: str
    tags: List[str]
    metadata: Optional[Dict[str, Any]]
    created_at: Optional[str]
    relevance_score: float
    usage_boost: float
    helpfulness_boost: float
    recency_boost: float
```

### MemoryMetadata (TypedDict)

```python
class MemoryMetadata(TypedDict, total=False):
    tags: List[str]
    category: str
    entities: List[str]
    importance: float
    summary: str
```

### CategorySummary (TypedDict)

```python
class CategorySummary(TypedDict):
    count: int
    avg_score: float
    summary: str
```
