"""
RecallBricks - Basic Usage Example

This example demonstrates both authentication methods:
1. API key - for user-level access
2. Service token - for server-to-server access
"""

from recallbricks import RecallBricks

# Option 1: Initialize with API key (user-level access)
memory = RecallBricks(api_key="rb_dev_zrWnAmVlGkbtNwy0wyfG_secret_2025")

# Option 2: Initialize with service token (server-to-server access)
# Uncomment to use service token instead:
# memory = RecallBricks(service_token="rbk_service_xxx")

print(f"Authenticated using: {'service token' if memory.service_token else 'API key'}")

# Save a memory
print("Saving memory...")
result = memory.save("This is a test memory from the Python SDK")
print(f"Memory saved with ID: {result.get('id')}")

# Get all memories
print("\nRetrieving all memories...")
memories = memory.get_all(limit=5)
print(f"Found {len(memories)} memories:")
for m in memories:
    print(f"  - {m['text'][:50]}...")

# Search memories
print("\nSearching for 'Python SDK'...")
results = memory.search("Python SDK")
print(f"Found {len(results)} matching memories")

# Check rate limit
print("\nChecking rate limit...")
status = memory.get_rate_limit()
print(f"API Usage: {status['remaining']}/{status['limit']} ({status['percentUsed']}% used)")
print(f"Resets at: {status['reset']}")
