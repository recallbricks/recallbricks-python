# RecallBricks Python SDK Documentation

**Version 1.5.1** | [GitHub](https://github.com/recallbricks/recallbricks-python) | [PyPI](https://pypi.org/project/recallbricks/)

The enterprise-grade memory layer for AI. Persistent, intelligent memory across all AI models with autonomous agent features.

## Documentation

| Document | Description |
|----------|-------------|
| [Quickstart](./quickstart.md) | Get started in under 5 minutes |
| [API Reference](./api-reference.md) | Complete API documentation |
| [Autonomous Features](./autonomous-features.md) | Agent memory & cognition clients |
| [Examples](./examples.md) | Working code examples |
| [Migration Guide](./migration.md) | Upgrade between versions |

## Installation

```bash
pip install recallbricks==1.5.1
```

## Quick Example

```python
from recallbricks import RecallBricks

# Initialize
rb = RecallBricks(api_key="rb_dev_your_key")

# Learn with automatic metadata extraction
result = rb.learn("User prefers dark mode and TypeScript")
print(f"Auto-tags: {result['metadata']['tags']}")

# Recall with semantic search
memories = rb.recall("user preferences", organized=True)
for category, info in memories.get('categories', {}).items():
    print(f"{category}: {info['summary']}")
```

## Features

### Core Memory Operations
- **save()** - Store memories with manual tags
- **learn()** - Store with auto-extracted metadata (tags, categories, entities)
- **recall()** - Semantic search with optional organization
- **search()** - Simple semantic search
- **predict_memories()** - Predict useful memories
- **suggest_memories()** - Context-aware suggestions

### Autonomous Agent SDK
Nine specialized clients for building truly autonomous AI agents:

| Client | Purpose |
|--------|---------|
| WorkingMemoryClient | Short-term context management |
| ProspectiveMemoryClient | Scheduled tasks & reminders |
| MetacognitionClient | Self-awareness & reasoning |
| MemoryTypesClient | Episodic, semantic, procedural memory |
| GoalsClient | Hierarchical goal tracking |
| HealthClient | Performance monitoring |
| UncertaintyClient | Confidence calibration |
| ContextClient | Session management |
| SearchClient | Advanced search |

```python
from recallbricks.autonomous import WorkingMemoryClient, GoalsClient

working_memory = WorkingMemoryClient(api_key="rb_dev_xxx")
working_memory.store(
    agent_id="agent_123",
    content="User context here",
    priority=0.8
)
```

## Support

- **Documentation**: https://recallbricks.com/docs
- **GitHub Issues**: https://github.com/recallbricks/recallbricks-python/issues
- **Email**: support@recallbricks.com

## License

MIT License
