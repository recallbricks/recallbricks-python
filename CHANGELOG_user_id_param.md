# Changelog: user_id Parameter Support

## Summary
Added `user_id` parameter support to the `save()` method to enable proper service token authentication.

## Changes Made

### 1. Updated `save()` Method Signature
**File**: `recallbricks/client.py:206-215`

Added `user_id` parameter:
```python
def save(
    self,
    text: str,
    user_id: Optional[str] = None,  # NEW PARAMETER
    source: str = "api",
    project_id: str = "default",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    max_retries: int = 3
) -> Dict[str, Any]:
```

### 2. Added Validation Logic
**File**: `recallbricks/client.py:243-257`

- **Service Token Validation**: Enforces `user_id` requirement when using service token
- **Format Validation**: Validates `user_id` is a non-empty string
- **Input Sanitization**: Sanitizes `user_id` to prevent injection attacks (max 256 chars)

```python
# Validate user_id when using service token
if self.service_token and not user_id:
    raise ValueError(
        "user_id is required when using service token authentication. "
        "Please provide a user_id parameter to identify the user."
    )

# Validate user_id format if provided
if user_id is not None:
    if not isinstance(user_id, str):
        raise TypeError(f"user_id must be a string, got {type(user_id).__name__}")
    if not user_id.strip():
        raise ValueError("user_id cannot be empty")
    user_id = self._sanitize_input(user_id, max_length=256)
```

### 3. Updated Payload Construction
**File**: `recallbricks/client.py:265-267`

Include `user_id` in request payload when provided:
```python
# Include user_id in payload if provided
if user_id:
    payload["user_id"] = user_id
```

### 4. Enhanced Documentation
**File**: `recallbricks/client.py:216-242`

Updated docstring with:
- Description of `user_id` parameter
- When it's required vs optional
- Usage examples for both auth methods
- Raises section for validation errors

### 5. Updated Class Documentation
**File**: `recallbricks/client.py:21-37`

Added note about `user_id` requirement in service token example.

## Behavior

### With Service Token
- `user_id` is **REQUIRED**
- Raises `ValueError` if not provided
- Validates and sanitizes the `user_id` value

### With API Key
- `user_id` is **OPTIONAL**
- Uses authenticated user by default when not provided
- Can override with explicit `user_id` if needed

## Validation Rules

1. **Type Check**: `user_id` must be a string
2. **Empty Check**: `user_id` cannot be empty/whitespace
3. **Length Limit**: Maximum 256 characters (after sanitization)
4. **Sanitization**: Removes control characters and null bytes

## Testing

Created comprehensive test suite in `test_user_id_param.py`:
- Service token requires user_id validation
- API key optional user_id validation
- Empty string validation
- Type validation
- Payload inclusion verification

All tests passed successfully.

## Examples

### Service Token (user_id required)
```python
from recallbricks import RecallBricks

rb = RecallBricks(service_token="rbk_service_xxx")
rb.save("User preferences", user_id="user_123")
```

### API Key (user_id optional)
```python
from recallbricks import RecallBricks

rb = RecallBricks(api_key="rb_dev_xxx")
rb.save("User preferences")  # Uses authenticated user
rb.save("Override", user_id="other_user")  # Optional override
```

## Files Modified
- `recallbricks/client.py` - Main implementation

## Files Created
- `test_user_id_param.py` - Validation tests
- `example_service_token_user_id.py` - Usage examples
- `CHANGELOG_user_id_param.md` - This file

## Breaking Changes
None - All changes are backward compatible. Existing API key usage without `user_id` continues to work.
