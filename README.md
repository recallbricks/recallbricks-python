# RecallBricks Python SDK

The Memory Layer for AI - Persistent memory across all AI models.

## Installation
```bash
pip install recallbricks
```

## Quick Start
```python
from recallbricks import RecallBricks

rb = RecallBricks("your-api-key")

# Create a memory
memory = rb.create_memory(
    text="User prefers dark mode",
    tags=["preference", "ui"]
)

# Search memories
results = rb.search("dark mode", limit=5)
for memory in results:
    print(memory.text)
```

## Features

### Relationship Support

RecallBricks supports memory relationships to build connected knowledge graphs:

```python
from recallbricks import RecallBricks

rb = RecallBricks("your-api-key")

# Create a memory
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

## Documentation

Visit https://recallbricks.com/docs for full documentation.

## License

MIT
