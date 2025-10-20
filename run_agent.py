# run_agent.py
from Untapped_Resource_Agent import ResourceAgent
import sys


def main():
    print("--- Initializing Resource Agent ---")
    try:
        # Initialize the agent class
        agent = ResourceAgent()
        print("Agent initialized successfully.")
        
        while True:
            # --- Get User Input ---
            user_input = input("\nWhat resources are you looking for? (Type 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                print("Exiting Resource Agent. Goodbye!")
                break
            
            if not user_input.strip():
                print("Please enter a query.")
                continue

            print(f"\n--- Running Query: '{user_input}' ---")
            
            # --- Invoke the Agent ---
            try:
                response = agent.find_resources(user_input)      
                print("\n--- Agent Response ---")
                print(response)
                print("----------------------")
            
            except ValueError as e:
                # Catches the ValueError raised by find_resources if query is empty
                print(f"Error: {e}", file=sys.stderr)
            except Exception as e:
                # Catches potential errors during tool execution or LLM interaction
                print(f"An error occurred during agent execution: {e}", file=sys.stderr)

    except ValueError as e:
        # Catches the initial error if API keys are missing
        print(f"Initialization Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()