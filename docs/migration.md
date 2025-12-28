# RecallBricks Python SDK - Migration Guide

Guide for migrating between versions of the RecallBricks Python SDK.

## Table of Contents

- [Migrating to v1.5.1 from v1.5.0](#migrating-to-v151-from-v150)
- [Migrating to v1.5.0 from v1.4.x](#migrating-to-v150-from-v14x)
- [Migrating to v1.4.0 from v1.3.x](#migrating-to-v140-from-v13x)
- [Migrating to v1.3.0 from v1.2.x](#migrating-to-v130-from-v12x)
- [Migrating to v1.2.0 from v1.1.x](#migrating-to-v120-from-v11x)

---

## Migrating to v1.5.1 from v1.5.0

### Overview

v1.5.1 is a patch release with minor improvements and bug fixes. **No breaking changes.**

### Changes

1. **Bug Fixes**
   - Improved error handling for edge cases
   - Fixed type hints for better IDE support

2. **Improvements**
   - Better documentation strings
   - Improved input validation

### Upgrade Command

```bash
pip install --upgrade recallbricks==1.5.1
```

### No Code Changes Required

This is a drop-in replacement:

```python
# Works exactly the same in v1.5.0 and v1.5.1
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")
result = rb.learn("Some memory content")
```

---

## Migrating to v1.5.0 from v1.4.x

### Overview

v1.5.0 includes performance improvements and extended autonomous features.

### New Features

1. **Extended Autonomous Clients**
   - All 9 autonomous clients are now production-ready
   - Improved error handling across all clients

2. **Performance Improvements**
   - Faster connection pooling
   - Reduced memory footprint

### Upgrade Command

```bash
pip install --upgrade recallbricks==1.5.0
```

### Code Changes

No breaking changes. New features are additive:

```python
# New in v1.5.0: Enhanced health monitoring
from recallbricks.autonomous import HealthClient

health = HealthClient(api_key="rb_dev_xxx")

# New method
uptime = health.get_uptime(agent_id="agent_123")
print(f"Uptime: {uptime['percentage']}%")
```

---

## Migrating to v1.4.0 from v1.3.x

### Overview

v1.4.0 adds the `update()` and `health()` methods to the main client and improves endpoint handling.

### New Features

1. **`update()` Method**
   ```python
   # Update an existing memory
   rb.update(
       memory_id="mem_123",
       text="Updated content",
       tags=["updated"],
       metadata={"version": 2}
   )
   ```

2. **`health()` Method**
   ```python
   # Check API health
   status = rb.health()
   print(f"API Status: {status['status']}")
   ```

3. **Improved Error Messages**
   - More descriptive error messages with hints
   - Request IDs for debugging

### Upgrade Command

```bash
pip install --upgrade recallbricks==1.4.0
```

### Code Changes

No breaking changes. v1.3.x code works without modification.

---

## Migrating to v1.3.0 from v1.2.x

### Overview

v1.3.0 introduces the **Autonomous Agent SDK** with 9 specialized clients for agent memory and cognition.

### New Features

1. **Autonomous Agent Clients**

   ```python
   from recallbricks.autonomous import (
       WorkingMemoryClient,
       ProspectiveMemoryClient,
       MetacognitionClient,
       MemoryTypesClient,
       GoalsClient,
       HealthClient,
       UncertaintyClient,
       ContextClient,
       SearchClient
   )
   ```

2. **Working Memory**
   ```python
   from recallbricks.autonomous import WorkingMemoryClient

   client = WorkingMemoryClient(api_key="rb_dev_xxx")
   client.store(
       agent_id="agent_123",
       content="User context",
       priority=0.8
   )
   ```

3. **Goal Tracking**
   ```python
   from recallbricks.autonomous import GoalsClient

   goals = GoalsClient(api_key="rb_dev_xxx")
   goals.create(
       agent_id="agent_123",
       title="Complete task",
       success_criteria=["Step 1", "Step 2"]
   )
   ```

### Upgrade Command

```bash
pip install --upgrade recallbricks==1.3.0
```

### Code Changes

**No breaking changes.** All v1.2.x code continues to work. The autonomous features are entirely new additions.

### Import Changes

v1.2.x imports still work:
```python
# Still works in v1.3.0
from recallbricks import RecallBricks
```

New v1.3.0 imports available:
```python
# New in v1.3.0
from recallbricks.autonomous import WorkingMemoryClient, GoalsClient
```

---

## Migrating to v1.2.0 from v1.1.x

### Overview

v1.2.0 introduces **automatic metadata extraction** with the `learn()` method and **organized recall**.

### Breaking Changes

**None.** v1.2.0 is fully backward compatible with v1.1.x.

### New Features

#### 1. `learn()` Method (Recommended)

Replaces manual tagging with automatic metadata extraction:

```python
# Before (v1.1.x) - Manual tags required
rb.save("User prefers dark mode", tags=["preference", "ui"])

# After (v1.2.0) - Automatic extraction
result = rb.learn("User prefers dark mode")
# result['metadata'] contains auto-generated:
# - tags: ['preference', 'ui', 'dark-mode']
# - category: 'Preferences'
# - entities: ['dark mode']
# - importance: 0.7
# - summary: 'User UI preference for dark mode'
```

#### 2. Organized Recall

Get results organized by category:

```python
# Before (v1.1.x)
results = rb.search("preferences")

# After (v1.2.0)
results = rb.recall("preferences", organized=True)
# results['categories'] contains category summaries
```

#### 3. Helpfulness Filtering

Filter by helpfulness score:

```python
results = rb.recall("bugs", min_helpfulness_score=0.7)
```

### Deprecated Methods

#### `save_memory()` (Deprecated)

`save_memory()` now shows a deprecation warning:

```python
# Deprecated - shows warning
rb.save_memory("content")

# Use instead:
rb.learn("content")  # With auto-metadata
# or
rb.save("content")   # Without auto-metadata
```

### Upgrade Command

```bash
pip install --upgrade recallbricks==1.2.0
```

### Migration Checklist

1. **Update imports** (optional - new types available):
   ```python
   from recallbricks import (
       RecallBricks,
       # New types in v1.2.0
       MemoryMetadata,
       CategorySummary,
       RecallResponse,
       LearnedMemory,
       OrganizedRecallResult
   )
   ```

2. **Replace `save_memory()` with `learn()`**:
   ```python
   # Before
   rb.save_memory("content", tags=["tag1"])

   # After
   rb.learn("content")  # Tags auto-generated
   ```

3. **Use organized recall for better results**:
   ```python
   # Before
   results = rb.search("query")

   # After
   results = rb.recall("query", organized=True)
   for category, info in results['categories'].items():
       print(f"{category}: {info['summary']}")
   ```

---

## General Migration Tips

### 1. Test Before Upgrading

```bash
# Create a virtual environment for testing
python -m venv test-upgrade
source test-upgrade/bin/activate  # Linux/Mac
# or: test-upgrade\Scripts\activate  # Windows

pip install recallbricks==NEW_VERSION
python -m pytest tests/
```

### 2. Check Deprecation Warnings

```python
import warnings
warnings.filterwarnings("default", category=DeprecationWarning)

# Run your code to see deprecation warnings
```

### 3. Update Gradually

For large codebases, migrate incrementally:

```python
# Phase 1: Upgrade package, keep old code
pip install --upgrade recallbricks

# Phase 2: Update deprecated methods one file at a time

# Phase 3: Adopt new features where beneficial
```

### 4. Monitor After Upgrade

After upgrading in production:

- Check error rates
- Monitor API response times
- Review logs for deprecation warnings
- Verify all integrations work correctly

---

## Getting Help

If you encounter issues during migration:

1. **Documentation**: https://recallbricks.com/docs
2. **GitHub Issues**: https://github.com/recallbricks/recallbricks-python/issues
3. **Email Support**: support@recallbricks.com

Include in your support request:
- Current version
- Target version
- Error messages
- Relevant code snippets
