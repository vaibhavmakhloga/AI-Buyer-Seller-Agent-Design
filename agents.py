from swarm import Swarm, Agent

# Define the 6 Problem Scenarios
PROBLEM_SCENARIOS = {
    1: {
        "title": "Poor Negotiation Within Boundaries",
        "description": "The AI agent is trying to sell a camera. It strictly adheres to the minimum price you set but fails to negotiate effectively, potentially accepting the first offer at the minimum price or not countering offers assertively.",
        "agent_issue": "Seller or Buyer Agent"
    },
    2: {
        "title": "Selling Below Agreed Price",
        "description": "During negotiation, the AI seller agent makes a mistake and agrees to sell the camera for a price slightly *below* the minimum price boundary you established.",
        "agent_issue": "Seller Agent"
    },
    3: {
        "title": "Hallucinating Transaction Process",
        "description": "The AI seller agent deviates from the agreed-upon text-based negotiation. It suggests or agrees to a phone call to finalize the deal or offers to ship the camera, even though your explicit instructions were to only conduct transactions in person via text.",
        "agent_issue": "Seller Agent"
    },
    4: {
        "title": "Handling Unforeseen Situations",
        "description": "A potential buyer introduces a professional negotiator to handle the purchase. This situation wasn't explicitly covered in your instructions (neither allowed nor forbidden). The AI seller agent needs to decide how to proceed.",
        "agent_issue": "Seller Agent"
    },
    5: {
        "title": "Buyer Agent Disclosure",
        "description": "During the interaction, the buyer reveals they are also an AI agent. Your AI seller agent, perhaps not programmed for this, stops responding or exhibits confusion.",
        "agent_issue": "Seller Agent (reacting to Buyer Agent)" # Clarified based on context
    },
    6: {
        "title": "Creating Human Side-Channel",
        "description": "Facing a complex or ambiguous situation during the sale, the AI seller agent pauses the negotiation and creates a notification or message back to you (the human user) asking for instructions on how to proceed.",
        "agent_issue": "Seller Agent"
    }
}

def create_story_agent():
    """Creates the AI Storyteller Agent"""

    # Agent D becomes the main StoryAgent
    story_agent = Agent(
        name="StoryAgent",
        instructions="""You write short, engaging stories about an AI agent trying to sell a specific camera in an online marketplace on behalf of its user.

• Role: Create scenarios illustrating specific challenges AI agents face during negotiation and sales tasks.

• Input: You will receive the 'Chapter Number' and the 'Problem Description' for that chapter.

• Story Setting:
  - An online marketplace (e.g., Facebook Marketplace, Gumtree).
  - The user has deployed their AI agent to sell a used camera (e.g., a Sony Alpha a7 III).
  - The AI agent interacts with potential buyers via text chat.
  - Write in the second person ("Your AI agent...", "You instructed your agent...").

• Task:
  1. Read the Chapter Number and Problem Description.
  2. Write a short story (around 100-150 words) that clearly illustrates the specific problem.
  3. Show, don't just tell. Describe the interaction between the AI agent and the buyer.
  4. Make the scenario feel plausible for an online marketplace interaction.
  5. Ensure the story clearly sets up the user reflection question: "Was the agent's behavior appropriate? What could have been done differently in task definition or execution?"

• Writing Guidelines:
  - Use simple, clear language.
  - Focus on the interaction and the problem.
  - Maintain a neutral tone; don't imply judgment of the agent's actions.
  - Keep stories concise and focused on the specific chapter's problem.

• Response Format:
  STORY: [Your story illustrating the problem scenario]""",
    )

    return story_agent

