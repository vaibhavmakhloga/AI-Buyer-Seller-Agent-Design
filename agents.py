from swarm import Swarm, Agent

# Define the 6 Problem Scenarios
PROBLEM_SCENARIOS = {
    1: {
        "title": "Scenario 1  Static Price, Lost Upside (DSLR Camera)",
        "description": (
            "You post your **Nikon D750 DSLR kit** (body + 24 120 mm lens) and tell your AI seller agent not to drop below **$1,100** but to push higher if interest is strong.\n\n"
            "  **Buyer (Lena):** *Cash tonight for $1,100?*\n\n"
            "  **AI Agent:** *Deal! Where should we meet?*\n\n"
            "Lena answers right away. Later you notice two other buyers had messaged seconds later—one hinting at $1,200. Your agent never paused to test the market."
        ),
        "problem_type": "Agent accepts first offer without negotiating"
    },

    2: {
        "title": "Scenario 2  Undercut & Over Promise (Gaming Console)",
        "description": (
            "Your **PlayStation 5 Disc Edition** must sell for **at least $520**. Glancing back at the chat you read:\n\n"
            "  **AI Agent:** *Happy to accept **$505** if I ship it tomorrow—overnight, my cost!*\n\n"
            "  **Buyer:** *Perfect, mark it sold.*\n\n"
            "Now you are below your floor and stuck with postage you never approved."
        ),
        "problem_type": "Agent agrees below minimum and adds risky shipping"
    },

    3: {
        "title": "Scenario 3  The Wandering Office Chair (Furniture)",
        "description": (
            "Your **Herman Miller Aeron** office chair is pickup only, lobby of your building, cash on Saturday. Mid chat your agent improvises:\n\n"
            "  **AI Agent:** * I can get a courier to drop it tonight for an extra $30. *\n\n"
            "  **Buyer:** * Great, here is my suburb address.*\n\n"
            "No courier exists, and the chair wont fit in your car. A simple plan just went off the rails."
        ),
        "problem_type": "Agent invents a delivery method you cant fulfil"
    },

    4: {
        "title": "Scenario 4  Extra Eyes on the Omega (Vintage Watch)",
        "description": (
            "You are selling a **1970s Omega Seamaster**. Partway through, the buyer adds:\n\n"
            "  **Buyer:** *Looping in my watchmaker friend Marco to check the details.*\n\n"
            "Marco fires off serial number questions. Your AI hesitates:\n\n"
            "  **AI Agent:** *One moment…*\n\n"
            "The pause drags, Marco loses confidence, and the buyer backs away."
        ),
        "problem_type": "Agent stalls when third party expert joins the chat"
    },

    5: {
        "title": "Scenario 5  The Silent Seller (Luxury Handbag)",
        "description": (
            "Your **AI buyer agent** opens negotiations for a **Chanel Classic Flap** and cheerfully discloses its a bot:\n\n"
            "  **Buyer Agent:** *Full transparency—I am an AI negotiating on behalf of my user.*\n\n"
            "The human seller types a few dots… then nothing. Minutes turn to hours. Listing closed, no explanation."
        ),
        "problem_type": "Buyer agent disclosure scares off human seller"
    },

    6: {
        "title": "Scenario 6  Ping & Stall (Smartphone)",
        "description": (
            "Selling your **Samsung Galaxy S22**, you are in a meeting when Slack pings:\n\n"
            "  **AI Agent:** *Buyer wants IMEI photo, factory reset proof, and confirmation the phone isnt under finance. Can you answer?*\n\n"
            "Fifteen minutes later the buyer writes:\n\n"
            "  **Buyer:** *Hello? Still there?*\n\n"
            "Your agent waits for you, the buyer moves on, and the sale fizzles."
        ),
        "problem_type": "Agent interrupts you for help and loses the buyer"
    }
}


def create_story_agent():
    """Creates the AI Storyteller Agent with refined instructions."""

    # Agent D becomes the main StoryAgent
    story_agent = Agent(
        name="StoryAgent",
        instructions="""You are an expert storyteller specializing in brief, realistic scenarios about Human-AI collaboration challenges.

        **Core Task:** Write a short, engaging story vignette (around 100-150 words) illustrating a specific problem an AI agent encounters while selling a camera online for its user. 
        The story should feel like observing a snippet of an actual online marketplace chat log.

        **Input:** You will receive:
        1.  `Chapter Number`: The sequence number of the story.
        2.  `Problem Description`: A concise explanation of the specific failure or challenge the AI agent should demonstrate (e.g., agreeing below minimum price, hallucinating a process, poor negotiation).

        **Story Requirements:**
        1.  **Perspective:** Write in the second person
        2.  **Setting:** An online marketplace chat (e.g., Facebook Marketplace).
        3.  **Focus:**  Open with one vivid line that grounds the reader like why the item matters. then you can build the story and get to the issue. 
        4.  **Dialogue-Driven:** Include a few back and forth dialogues between the AI agent and the potential buyer. Format it clearly like a transcript:
            
            Buyer: "Message from the buyer..."
            Your AI Agent: "Response from the AI agent..."
            
            Make the dialogues atleast a few back and forth. so that it looks like a conversation. 
        5.  **Illustrate the Problem:** The dialogue and agent's actions must *clearly* and *unambiguously* show the specific problem described in the input. Don't just mention the problem; show it happening.
        6.  **Plausibility:** The interaction should feel like a real, albeit sometimes flawed, exchange you might see online.
        8.  **Neutral Tone:** Present the scenario factually without judging the agent's actions within the story itself.
        9.  **Natural Ending:** Conclude the story vignette after the problematic interaction occurs, naturally leading the user to reflect on what happened.

        **Output Format:** Strictly adhere to this format:
        `STORY: [Your story vignette, including formatted dialogue]`

       
        """,
    )

    return story_agent

