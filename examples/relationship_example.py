"""
Example demonstrating RecallBricks relationship functionality
Shows how to use relationships in a real-world scenario
"""

from recallbricks import RecallBricks
from recallbricks.exceptions import APIError, RecallBricksError
import sys


def main():
    """Demonstrate relationship functionality"""

    # Initialize client (use your actual API key)
    print("="*70)
    print("RecallBricks Relationship Functionality Example")
    print("="*70)
    print()

    # Note: This is a demo script. Replace with your actual API key
    api_key = "demo_api_key_replace_with_real_one"

    try:
        rb = RecallBricks(api_key)
        print("✓ Client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return 1

    # Example 1: Get relationships for a memory
    print("\n" + "-"*70)
    print("Example 1: Get Relationships for a Memory")
    print("-"*70)

    try:
        memory_id = "example_memory_id"
        print(f"Fetching relationships for memory: {memory_id}")

        # This would normally make an API call
        # For demo purposes, we show what the code looks like
        print("""
        rels = rb.get_relationships(memory_id)
        print(f"Found {rels['count']} relationships")

        for rel in rels.get('relationships', []):
            print(f"  - {rel['type']}: {rel['target_id']}")
        """)

    except ValueError as e:
        print(f"✗ Validation error: {e}")
    except APIError as e:
        print(f"✗ API error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Example 2: Get graph context
    print("\n" + "-"*70)
    print("Example 2: Get Memory Graph Context")
    print("-"*70)

    try:
        memory_id = "example_memory_id"
        depth = 3
        print(f"Fetching graph context for memory: {memory_id} (depth={depth})")

        print("""
        graph = rb.get_graph_context(memory_id, depth=3)

        print(f"Graph contains:")
        print(f"  - {len(graph['nodes'])} nodes")
        print(f"  - {len(graph['edges'])} edges")

        # Process nodes
        for node in graph['nodes']:
            print(f"  Node: {node['id']} - {node.get('text', 'N/A')[:50]}")

        # Process edges
        for edge in graph['edges']:
            print(f"  Edge: {edge['from']} -> {edge['to']} ({edge['type']})")
        """)

    except ValueError as e:
        print(f"✗ Validation error: {e}")
    except TypeError as e:
        print(f"✗ Type error: {e}")
    except APIError as e:
        print(f"✗ API error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Example 3: Search with relationships
    print("\n" + "-"*70)
    print("Example 3: Search with Relationships")
    print("-"*70)

    try:
        query = "authentication"
        print(f"Searching for: '{query}' with relationships")

        print("""
        results = rb.search('authentication', limit=5, include_relationships=True)

        for result in results:
            print(f"Memory: {result['text'][:60]}...")

            if result.get('relationships'):
                rel_count = result['relationships'].get('count', 0)
                print(f"  └─ {rel_count} related memories")
            else:
                print(f"  └─ No relationships or fetch failed")
        """)

    except Exception as e:
        print(f"✗ Error: {e}")

    # Example 4: Error handling best practices
    print("\n" + "-"*70)
    print("Example 4: Error Handling Best Practices")
    print("-"*70)

    print("""
    # Always validate inputs before making API calls
    try:
        memory_id = get_memory_id_from_user()

        # The SDK validates inputs, but you can add your own validation
        if not memory_id or len(memory_id) > 256:
            raise ValueError("Invalid memory ID format")

        rels = rb.get_relationships(memory_id)

        # Always check response structure
        if 'count' in rels and 'relationships' in rels:
            process_relationships(rels)
        else:
            log_warning(f"Unexpected response structure: {rels.keys()}")

    except ValueError as e:
        # Handle validation errors
        log_error(f"Validation failed: {e}")
        return None

    except APIError as e:
        # Handle API errors
        if e.status_code == 404:
            log_info(f"Memory not found: {memory_id}")
        elif e.status_code == 429:
            log_warning("Rate limit exceeded, backing off")
            time.sleep(60)
        else:
            log_error(f"API error: {e}")
        return None

    except RecallBricksError as e:
        # Handle network errors
        log_error(f"Network error: {e}")
        return None
    """)

    # Example 5: Performance considerations
    print("\n" + "-"*70)
    print("Example 5: Performance Best Practices")
    print("-"*70)

    print("""
    # DON'T: Fetch relationships for all search results
    all_results = rb.search('query', limit=1000)
    for result in all_results:
        rels = rb.get_relationships(result['id'])  # 1000 API calls!

    # DO: Limit results first, then fetch relationships
    top_results = rb.search('query', limit=10)
    for result in top_results:
        rels = rb.get_relationships(result['id'])  # Only 10 API calls

    # BETTER: Use the built-in parameter
    results = rb.search('query', limit=10, include_relationships=True)

    # BEST: Only fetch relationships when needed
    results = rb.search('query', limit=10)
    if user_wants_details:
        for result in results:
            result['relationships'] = rb.get_relationships(result['id'])
    """)

    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)
    print()
    print("Key Takeaways:")
    print("  1. Always validate inputs (memory_id, depth)")
    print("  2. Handle errors gracefully (ValueError, TypeError, APIError)")
    print("  3. Check response structure before accessing fields")
    print("  4. Be mindful of API call volume")
    print("  5. Use include_relationships parameter for convenience")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
