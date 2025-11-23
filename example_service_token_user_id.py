"""
Example: Using service token with user_id parameter

This example demonstrates how to use the RecallBricks SDK with service token
authentication, which requires the user_id parameter.
"""

from recallbricks import RecallBricks

# Initialize with service token
# Note: Service tokens are used for server-to-server authentication
rb = RecallBricks(service_token="rbk_service_YOUR_TOKEN_HERE")

# When using service token, you MUST provide user_id
try:
    # This will raise ValueError
    rb.save("This will fail without user_id")
except ValueError as e:
    print(f"Error (expected): {e}")
    print()

# Correct usage: Provide user_id with service token
print("Saving memory with user_id...")
try:
    result = rb.save(
        text="User prefers dark mode and TypeScript",
        user_id="user_12345",  # Required for service token
        tags=["preferences", "ui"],
        metadata={"context": "settings"}
    )
    print(f"Success! Memory saved: {result}")
except Exception as e:
    print(f"Error: {e}")

# Multiple saves for different users
print("\nSaving memories for multiple users...")
users = [
    {"user_id": "user_001", "text": "Alice prefers Python and vim"},
    {"user_id": "user_002", "text": "Bob prefers JavaScript and VSCode"},
    {"user_id": "user_003", "text": "Carol prefers Rust and emacs"}
]

for user in users:
    try:
        result = rb.save(
            text=user["text"],
            user_id=user["user_id"]
        )
        print(f"  Saved for {user['user_id']}")
    except Exception as e:
        print(f"  Failed for {user['user_id']}: {e}")

print("\n" + "="*60)
print("Note: With API key authentication, user_id is optional")
print("="*60)

# With API key, user_id is optional (uses authenticated user)
rb_api_key = RecallBricks(api_key="rb_dev_YOUR_API_KEY_HERE")

try:
    # This works without user_id when using API key
    result = rb_api_key.save("User prefers dark mode")
    print("API key: Memory saved without user_id")
except Exception as e:
    print(f"Error: {e}")

try:
    # You can also provide user_id with API key if needed
    result = rb_api_key.save("Override user", user_id="custom_user_123")
    print("API key: Memory saved with explicit user_id")
except Exception as e:
    print(f"Error: {e}")
