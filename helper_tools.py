import time

# helper_tools.py

# This function allows you to construct messages for the openAI API to present them in a multi-turn format. It expects a 'memory_structure' 
# which can be taken with a function in the memory_handle module 

def construct_data(memory_structure, sys_prompt="You are an agent in an text adventure game, you have to interact with the CLI, figure  out what to do and how to interact these are your deep memories System Memory Overview:\n\n"):
    messages = []
    
    current_time_unix = int(time.time())
    formatted_time = time.ctime(current_time_unix)

    system_message_content = f"The current time is: {formatted_time} \n\n"

    # Construct System Message from long_term and base_memory
    system_message_content += f"{sys_prompt}\n\n"

    
    base_memory = memory_structure.get("base_memory", "No base memory available.")
    system_message_content += "Base Memory:\n"
    system_message_content += base_memory + "\n\n"

    long_term_memory = memory_structure.get("long_term", [])
    if long_term_memory:
        system_message_content += "Long-Term Memory:\n"
        for i, entry in enumerate(long_term_memory, 1):
            system_message_content += f"{i}. {entry}\n"
    else:
        system_message_content += "No long-term memory entries available.\n"

    system_message = {
        "role": "system",
        "content": [{"type": "text", "text": system_message_content}]
    }
    messages.append(system_message) # Prepend the system message


    short_term_memory = memory_structure.get("short_term", {}) # Safely get short_term, default to empty dict if missing

    for key, text in short_term_memory.items():
        role = key.split('_')[0] # Extract role from key like "user_12" -> "user"
        message_entry = {
            "role": role,
            "content": [{"type": "text", "text": text}]
        }
        messages.append(message_entry)
    return messages

