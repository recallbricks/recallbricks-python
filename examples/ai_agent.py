"""
RecallBricks - AI Agent Integration Example
Shows how to integrate RecallBricks with an AI agent
"""

from recallbricks import RecallBricks

class AIAgent:
    def __init__(self, api_key):
        self.memory = RecallBricks(api_key=api_key)
    
    def remember(self, information):
        """Save information to long-term memory"""
        self.memory.save(
            text=information,
            source="ai-agent",
            project_id="agent-memory"
        )
        print(f"í²¾ Remembered: {information}")
    
    def recall(self, query):
        """Search for relevant memories"""
        results = self.memory.search(query, limit=5)
        print(f"í·  Found {len(results)} relevant memories:")
        for r in results:
            print(f"  - {r['text']}")
        return results
    
    def process_conversation(self, user_input):
        """Process user input with memory context"""
        # First, recall relevant context
        context = self.recall(user_input)
        
        # Then save this interaction
        self.remember(f"User said: {user_input}")
        
        # Your AI logic here...
        return context

# Example usage
if __name__ == "__main__":
    agent = AIAgent(api_key="rb_dev_zrWnAmVlGkbtNwy0wyfG_secret_2025")
    
    # Agent remembers facts
    agent.remember("User prefers Python over JavaScript")
    agent.remember("User is building a SaaS product")
    agent.remember("User's timezone is EST")
    
    # Agent recalls when needed
    agent.recall("programming language")
    agent.recall("timezone")
