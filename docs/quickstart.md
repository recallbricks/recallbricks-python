# RecallBricks Python SDK - Quickstart Guide

Get started with the RecallBricks Python SDK in under 5 minutes.

## Installation

```bash
pip install recallbricks==1.5.1
```

## Environment Setup

Set your API key as an environment variable (recommended):

```bash
# Linux/macOS
export RECALLBRICKS_API_KEY="rb_dev_your_api_key_here"

# Windows (Command Prompt)
set RECALLBRICKS_API_KEY=rb_dev_your_api_key_here

# Windows (PowerShell)
$env:RECALLBRICKS_API_KEY="rb_dev_your_api_key_here"
```

## Basic Setup

### Option 1: API Key Authentication (User-Level Access)

```python
from recallbricks import RecallBricks

# Initialize with API key
rb = RecallBricks(api_key="rb_dev_your_api_key_here")
```

### Option 2: Service Token Authentication (Server-to-Server)

```python
from recallbricks import RecallBricks

# Initialize with service token
rb = RecallBricks(service_token="rbk_service_your_token_here")

# Note: user_id is required for all operations when using service token
```

### Using Environment Variables

```python
import os
from recallbricks import RecallBricks

rb = RecallBricks(api_key=os.environ.get("RECALLBRICKS_API_KEY"))
```

## Your First Memory

### Save a Memory

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")

# Save a simple memory
result = rb.save("User prefers dark mode and TypeScript for frontend development")
print(f"Memory saved with ID: {result['id']}")
```

### Save with Automatic Metadata Extraction

Use `learn()` for automatic tag, category, and entity extraction:

```python
# Learn automatically extracts metadata
result = rb.learn("Fixed authentication bug in the login flow using JWT refresh tokens")

print(f"ID: {result['id']}")
print(f"Auto-tags: {result['metadata']['tags']}")
print(f"Category: {result['metadata']['category']}")
print(f"Entities: {result['metadata']['entities']}")
print(f"Importance: {result['metadata']['importance']}")
```

### Recall Memories

```python
# Basic recall
results = rb.recall("authentication", limit=5)
for mem in results['memories']:
    print(f"- {mem['text']}")

# Organized recall with category summaries
results = rb.recall("user preferences", organized=True)
for category, info in results.get('categories', {}).items():
    print(f"{category}: {info['count']} memories")
```

### Search Memories

```python
# Semantic search
results = rb.search("dark mode settings", limit=10)
for mem in results['memories']:
    print(f"- {mem['text']}")
```

### Get All Memories

```python
# Retrieve all memories
all_memories = rb.get_all(limit=100)
print(f"Total memories: {all_memories['count']}")
```

## Quick Reference

| Operation | Method | Description |
|-----------|--------|-------------|
| Save memory | `rb.save(text)` | Save with manual tags |
| Learn memory | `rb.learn(text)` | Save with auto-extracted metadata |
| Recall | `rb.recall(query)` | Semantic search with optional organization |
| Search | `rb.search(query)` | Simple semantic search |
| Get all | `rb.get_all()` | Retrieve all memories |
| Get one | `rb.get(memory_id)` | Get specific memory |
| Update | `rb.update(memory_id, text=...)` | Update memory |
| Delete | `rb.delete(memory_id)` | Delete memory |

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
    rb = RecallBricks(api_key="rb_dev_xxx")
    memory = rb.save("Test memory")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}")
except APIError as e:
    print(f"API error ({e.status_code}): {e.message}")
except RecallBricksError as e:
    print(f"General error: {str(e)}")
```

## Next Steps

- [API Reference](./api-reference.md) - Complete API documentation
- [Autonomous Features](./autonomous-features.md) - Agent memory capabilities
- [Examples](./examples.md) - Working code examples
- [Migration Guide](./migration.md) - Upgrading from older versions
