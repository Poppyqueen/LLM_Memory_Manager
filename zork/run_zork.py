# run_zork.py

import subprocess
import time
import os
import select
import sys
from ai_handle import ai_bot
from memory_handle import memory_manager
# Now you can use ai_bot and memory_manager
import configparser

config = configparser.ConfigParser()


config.read('config.ini')
sleep_time = int(config['ADVENTURE']['action_sleep_time'])



shared_bot_instance = ai_bot()

# Initialize memory manager with the shared bot instance
memory_client = memory_manager(ai_bot_instance=shared_bot_instance, filepath="zork/game_memory_db.json")


# Start Zork in Frotz with proper terminal settings

process = subprocess.Popen(
    ["frotz", "zork/ZORK1.DAT"], # Changing this to any other Z-Machine game should be enough to set up the agent to play it.
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=os.environ.copy()  # Pass through environment variables
)


# Function to read game output with timeout
def read_output(timeout=60.0):
    output = ""
    start_time = time.time()
    
    # Use select to check if there's data available to read
    while time.time() - start_time < timeout:
        # Check if there's data ready to read (with a short timeout)
        ready_to_read, _, _ = select.select([process.stdout], [], [], 0.1)
        
        if process.stdout in ready_to_read:
            # Read a chunk of data
            chunk = os.read(process.stdout.fileno(), 4096).decode('utf-8', errors='replace')
            if not chunk:
                break
            output += chunk
        else:
            # If no data for a bit and we already have some output, break
            if output and time.time() - start_time > 0.5:
                break
    
    if output:
        print("\nZork says:", output)
        memory_client.save_to_memory(output,"short_term", "system")
        #memory_client.check()

        time.sleep(sleep_time) # Sleep in between actions

    return output

# Send AI-generated input
def send_input(command):
    if not command.endswith('\n'):
        command += '\n'  # Ensure command ends with newline
    
    #print("\nSending:", command.strip())
    try:
        process.stdin.write(command)
        process.stdin.flush()
    except:
        print("Error: Could not send input to Zork")

# Main function with improved control
def main():
    print("Starting Zork... (Give it a moment to initialize)")
    time.sleep(1)  # Give Frotz time to initialize
    
    # Read initial game intro
    game_text = read_output()
    if not game_text:
        print("WARNING: No initial output received from Zork. Check if Frotz is working correctly.")
    
    # Main game loop
    try:
        while process.poll() is None:  # Check if process is still running
            mem_structure=memory_client.get_memory_structure()
            ai_action, ai_thoughts = shared_bot_instance.adventure_response(mem_structure, "You are an AI agent in a text adventure game, you are tasked on exploring this environment via reasoning and commands to explore all it has to offer. For your response, make sure to only use commands that a CLI Text Adventure would recognize.")

            memory_snippet= f"Thoughts: {ai_thoughts}\n Action:{ai_action}"
            #print(f"this is our snippet! {memory_snippet}")
            print(f"Thoughts: {ai_thoughts}\n")
            print(f"Action: {ai_action}\n")
            time.sleep(5)  # Give Frotz time

            #ai_response = input("\nEnter your command (or 'quit' to exit): ")
            memory_client.save_to_memory(memory_snippet,"short_term","assistant")
            memory_client.check()

            time.sleep(2)

            
            if ai_action.lower() in ['quit', 'exit']:
                break
                
            send_input(ai_action)
            game_text = read_output()
    except KeyboardInterrupt:
        print("\nExiting game...")
    finally:
        # Clean up
        print("Cleaning up...")
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
        
        # Reset terminal
        if sys.platform != 'win32':
            os.system('stty sane')
        print("Game ended.")

if __name__ == "__main__":
    main()

