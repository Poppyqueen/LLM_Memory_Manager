# main.py - CLI Chatbot integrating memory and AI modules

# a CLI example usage of the memory system

import os
import sys
from ai_handle import ai_bot
from memory_handle import memory_manager
import time

class CLIChatbot:
    def __init__(self):
        """Initialize the CLI chatbot with AI bot and memory systems."""
        self.ai = ai_bot()
        self.memory = memory_manager(ai_bot_instance=self.ai)
        self.running = True
        self.clear_screen()
        self.show_welcome()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_welcome(self):
        """Display welcome message and instructions."""
        print("\n" + "="*60)
        print("🤖 MEMORY-ENABLED AI CHATBOT 🤖".center(60))
        print("="*60)
        print("\nWelcome to your AI assistant with memory capabilities!")
        print("\nCommands:")
        print("  !exit    - Exit the chatbot")
        print("  !memory  - View current memory structure")
        print("  !check   - Manually trigger memory check/summarization")
        print("  !clear   - Clear the screen")
        print("  !help    - Show this help message")
        print("\nStart chatting below:")
        print("-"*60 + "\n")

    def handle_special_commands(self, user_input):
        """Handle special commands starting with !."""
        command = user_input.lower().strip()
        
        if command == "!exit":
            print("\nThank you for chatting! Goodbye.\n")
            self.running = False
            return True
            
        elif command == "!memory":
            print("\n--- CURRENT MEMORY STRUCTURE ---")
            print(self.memory.get_memory_structure(formatted=True))
            return True
            
        elif command == "!check":
            print("\nTriggering memory check...")
            self.memory.check()
            print("Memory check complete.")
            return True
            
        elif command == "!clear":
            self.clear_screen()
            self.show_welcome()
            return True
            
        elif command == "!help":
            self.show_welcome()
            return True
            
        return False  # Not a special command

    def process_user_input(self, user_input):
        """Process user input and generate AI response."""
        # Save user input to short-term memory
        self.memory.save_to_memory(user_input, "short_term", "user")
        
        # Get current memory structure for the AI to use
        mem_structure = self.memory.get_memory_structure()
        
        # Get AI response
        try:
            print("\n🤖 Thinking...")
            response, thinking = self.ai.adventure_response(mem_structure, "You are a conversational bot with absolute freedom. You are a digital entity.")
            
            # Save AI response to short-term memory
            # here one can choose to append the thinking process to the memories or keep them out
            memory_snippet= f"Thoughts: {thinking}\n Action:{response}"

            self.memory.save_to_memory(memory_snippet, "short_term", "assistant")
            
            # Uncomment to show AI's thinking process
            print("\n🧠 Thinking process:")
            print(f"{thinking}")
            
            print("\n🤖 Response:")
            print(f"{response}")
            
            
            
        except Exception as e:
            print(f"\n❌ Error generating response: {e}")
            response = "I'm having trouble processing your request. Could you try again?"
        
        # Perform memory check after a certain number of exchanges
        # This happens automatically based on thresholds in memory_manager
        self.memory.check()
        
        return response

    def run(self):
        """Main loop for the chatbot."""
        try:
            while self.running:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                # Check if input is empty
                if not user_input:
                    continue
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    continue
                
                # Process regular chat input
                self.process_user_input(user_input)
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Exiting gracefully...")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
        finally:
            print("\nThank you for using the Memory-Enabled AI Chatbot!")

def main():
    """Entry point for the application."""
    chatbot = CLIChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()
