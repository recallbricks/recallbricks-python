"""
RecallBricks - Batch Operations Example
"""

from recallbricks import RecallBricks
import time

memory = RecallBricks(api_key="rb_dev_zrWnAmVlGkbtNwy0wyfG_secret_2025")

# Batch save multiple memories
memories_to_save = [
    "User prefers dark mode UI",
    "Project uses React and TypeScript",
    "Database is PostgreSQL",
    "Deployed on Vercel",
    "API built with FastAPI"
]

print("Saving batch of memories...")
for text in memories_to_save:
    memory.save(text, project_id="my-project", tags=["batch-import"])
    print(f"✓ Saved: {text}")
    time.sleep(0.1)  # Rate limiting courtesy

print(f"\n✅ Successfully saved {len(memories_to_save)} memories")

# Retrieve and organize
all_memories = memory.get_all()
print(f"\nTotal memories in system: {len(all_memories)}")

# Group by source
by_source = {}
for m in all_memories:
    source = m.get('source', 'unknown')
    by_source[source] = by_source.get(source, 0) + 1

print("\nMemories by source:")
for source, count in by_source.items():
    print(f"  {source}: {count}")
