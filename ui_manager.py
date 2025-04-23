class UIManager:
    @staticmethod
    def print_initialization():
        print("\n=== System Initialization ===")
        print("✓ Swarm client initialized")
        print("✓ Agent A (Parameter Identifier) initialized")
        print("✓ Agent B (Background Provider) initialized")
        print("✓ Agent C (Story Creator) initialized")
        
        print("\n" + "="*50)
        print("=== Interactive Social Proxy Story Generator ===")
        print("="*50)
        print("\nHelp design a better social proxy through storytelling")
        print("Type 'exit' to quit the program")
        print("-"*50)

    @staticmethod
    def get_user_input(is_initial=False):
        if is_initial:
            print("\n📝 Initial Design Parameter")
            print("What's an important feature for the social proxy robot?")
            print("Example: 'It should maintain eye contact during conversations'")
            return input("\n➤ Enter feature: ")
        else:
            print("\nBased on the story above:")
            print("- What new feature would you add?")
            print("- How would you enhance existing functionality?")
            print("- What aspect would you like to develop further?")
            return input("\n➤ Enter your design idea: ")

    @staticmethod
    def display_story_part(story):
        print("\n📖 Most Recent Story Part:")
        print("-"*30)
        print(story)
        print("-"*30)

    @staticmethod
    def display_parameter(parameter):
        print("\n🎯 Parameter Analysis:")
        print(parameter)

    @staticmethod
    def display_final_story(story, filename):
        print(f"\n✓ Session saved to {filename}")
        print("\n" + "="*50)
        print("=== Final Story & Design Evolution ===")
        print("="*50)
        print(story)
        print("\n" + "="*50)
        print("Design session completed...") 