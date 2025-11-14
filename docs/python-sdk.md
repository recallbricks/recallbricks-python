# RecallBricks Python SDK Documentation

## Overview

RecallBricks is the Memory Layer for AI - providing persistent memory across all AI models and autonomous agents.

## Installation

```bash
pip install recallbricks
```

## Quick Start

```python
from recallbricks import RecallBricks

# Initialize the client
rb = RecallBricks(api_key="your_api_key")

# Save a memory
rb.save("User prefers dark mode and TypeScript")

# Retrieve memories
memories = rb.get_all()
```

## Auto-Capture for Autonomous Agents

For autonomous agents that need to remember everything without manual intervention, RecallBricks provides automatic memory capture through decorators.

### Function Decorator

The `capture_function` decorator automatically saves function inputs and outputs, making it perfect for agent workflows where reliability is critical.

#### Basic Usage

```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="your_api_key")

@rb.capture_function()
def process_email(sender, subject):
    """Process an email and generate a response"""
    response = f"Processed email from {sender} about {subject}"
    # All inputs and outputs are automatically saved
    return response

# Use the function normally
result = process_email("boss@company.com", "Q4 Report")
```

#### Configuration Options

You can customize what gets captured:

```python
@rb.capture_function(
    save_inputs=True,   # Save function arguments (default: True)
    save_outputs=True,  # Save return values (default: True)
    include_errors=True # Save exceptions (default: True)
)
def analyze_data(data):
    # Your agent logic here
    return process_data(data)
```

#### Error Handling

The decorator automatically captures errors for debugging and analysis:

```python
@rb.capture_function(include_errors=True)
def risky_operation(value):
    if value < 0:
        raise ValueError("Value must be positive")
    return value * 2

try:
    result = risky_operation(-5)
except ValueError:
    # Error is automatically saved to RecallBricks
    pass
```

### Automatic Retry with Exponential Backoff

All save operations include automatic retry logic to ensure reliability in production environments:

```python
# Retries automatically enabled (default: 3 attempts)
rb.save("Important agent decision", max_retries=3)

# The retry schedule:
# - Attempt 1: Immediate
# - Attempt 2: Wait 1 second
# - Attempt 3: Wait 2 seconds
# - Attempt 4: Wait 4 seconds
```

You can customize retry behavior:

```python
# Disable retries for non-critical data
rb.save("Debug log", max_retries=1)

# Increase retries for critical data
rb.save("Customer order", max_retries=5)
```

## Core API Methods

### Save a Memory

```python
rb.save(
    text="Memory content",
    source="api",           # Optional: source identifier
    project_id="default",   # Optional: project identifier
    tags=["important"],     # Optional: list of tags
    metadata={"key": "value"},  # Optional: additional metadata
    max_retries=3           # Optional: retry attempts
)
```

### Get All Memories

```python
# Get all memories
all_memories = rb.get_all()

# Get with limit
recent_memories = rb.get_all(limit=10)
```

### Search Memories

```python
# Search by text
results = rb.search("dark mode", limit=5)
```

### Get a Specific Memory

```python
memory = rb.get(memory_id="123e4567-e89b-12d3-a456-426614174000")
```

### Delete a Memory

```python
rb.delete(memory_id="123e4567-e89b-12d3-a456-426614174000")
```

### Check Rate Limit

```python
status = rb.get_rate_limit()
print(f"Remaining: {status['remaining']}/{status['limit']}")
```

## Best Practices for Autonomous Agents

### 1. Use Auto-Capture for Critical Functions

Decorate all functions that make important decisions or interact with external systems:

```python
@rb.capture_function()
def make_trade_decision(market_data):
    # Critical agent decision - automatically saved
    return analyze_and_trade(market_data)

@rb.capture_function()
def send_customer_email(customer_id, message):
    # Customer interaction - automatically saved
    return email_service.send(customer_id, message)
```

### 2. Selective Capture

For high-frequency operations, capture only what matters:

```python
@rb.capture_function(save_inputs=False, save_outputs=True)
def get_current_price():
    # Don't save inputs (no args), but save the result
    return fetch_price_from_api()
```

### 3. Error Tracking

Always enable error tracking for debugging agent behavior:

```python
@rb.capture_function(include_errors=True)
def autonomous_task():
    # Any errors are captured for post-mortem analysis
    perform_complex_operation()
```

### 4. Combine with Manual Saves

Use auto-capture for function-level tracking and manual saves for high-level decisions:

```python
@rb.capture_function()
def process_step(data):
    return transform(data)

def agent_workflow():
    # Save high-level decision
    rb.save("Starting workflow: customer_onboarding")

    # Auto-captured
    result = process_step(data)

    # Save completion
    rb.save(f"Workflow completed: {result}")
```

## Error Handling

The SDK includes robust error handling:

```python
from recallbricks.exceptions import (
    AuthenticationError,
    RateLimitError,
    APIError,
    RecallBricksError
)

try:
    rb.save("Important memory")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}")
except APIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
except RecallBricksError as e:
    print(f"General error: {e}")
```

## Configuration

### Custom Base URL

For self-hosted or development environments:

```python
rb = RecallBricks(
    api_key="your_api_key",
    base_url="https://your-custom-domain.com"
)
```

## Support

For issues, feature requests, or questions:
- GitHub: https://github.com/recallbricks/recallbricks-python
- Documentation: https://recallbricks.com/docs
- Email: support@recallbricks.com
