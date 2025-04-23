from swarm import Swarm
from agents import create_agents
from story_manager import StoryManager
from ui_manager import UIManager

def main():
    # Initialize components
    client = Swarm()
    agent_a, agent_b, agent_c = create_agents()
    story_manager = StoryManager()
    ui = UIManager()

    # Setup UI
    ui.print_initialization()

    while True:
        # Get user input
        user_input = ui.get_user_input(not story_manager.current_story)
        if user_input.lower() == 'exit':
            filename = story_manager.save_session()
            ui.display_final_story(story_manager.get_complete_story(), filename)
            break

        story_manager.add_user_prompt(user_input)
        
        # Prepare message
        initial_message = {
            "role": "user",
            "content": user_input + (" [NEW STORY]" if not story_manager.current_story else " [CONTINUATION]")
        }
        
        if story_manager.current_story:
            initial_message["content"] += f"\n\nPrevious story:\n{''.join(story_manager.session_story)}"
        
        print("\n🔄 Processing...")
        
        # Run agents
        response_a = client.run(agent=agent_a, messages=[initial_message])
        parameter_info = response_a.messages[-1]["content"]
        #ui.display_parameter(parameter_info)
        
        response_c = client.run(
            agent=agent_c,
            messages=[
                initial_message,
                {"role": "assistant", "content": parameter_info}
            ]
        )
        context_info = response_c.messages[-1]["content"]
        
        response_b = client.run(
            agent=agent_b,
            messages=[
                initial_message,
                {"role": "system", "content": f"Parameter Info: {parameter_info}\nContext Info: {context_info}\nFull previous story: {''.join(story_manager.session_story)}"}
            ]
        )
        
        # Update story
        story_manager.add_story_segment(response_b.messages[-1]["content"])
        if story_manager.current_story:
            ui.display_story_part(story_manager.current_story)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()