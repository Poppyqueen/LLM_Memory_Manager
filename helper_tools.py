import time

# helper_tools.py

# This function allows you to construct messages for the openAI API to present them in a multi-turn format. It expects a 'memory_structure' 
# which can be taken with a function in the memory_handle module 


def construct_data(memory_structure, sys_prompt="You are an agent in an text adventure game, you have to interact with the CLI, figure  out what to do and how to interact these are your deep memories System Memory Overview:\n\n"):
    """
    Constructs the data to be sent to the OpenAI API for processing in a multi-turn format.
    It expects a memory structure and a system prompt.

    Creates an initial 'developer' message containing time, base prompt, base memory,
    and long-term memory. Then, processes short-term memory entries:
    'system_' and '0_system_' keys become separate 'system' messages.
    Other keys ('user_', 'assistant_', etc.) become messages with their corresponding roles.
    Messages are added in chronological order based on short-term keys.

    Args:
        memory_structure (dict): The dictionary representing the memory structure.
                                    Expected keys: 'base_memory', 'long_term', 'short_term'.
        sys_prompt (str): The base system prompt to include in the developer message.

    Returns:
        list: A list of message dictionaries formatted for the OpenAI API.
    """
    messages = []

    # --- Construct the initial 'developer' message (keeping original structure) ---
    current_time_unix = int(time.time())
    formatted_time = time.ctime(current_time_unix)

    system_message_content = f"The current time is: {formatted_time} \n\n"
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

    developer_message = {
        "role": "developer",
        "content": system_message_content
    }
    messages.append(developer_message) # Add the initial developer message

    # --- Process Short-Term Memory entries ---
    short_term_memory = memory_structure.get("short_term", {})

    # Sort keys to maintain chronological order for conversation turns
    # Assumes keys like "user_timestamp", "assistant_timestamp", "0_system_timestamp", etc.
    # Sort keys based on the numeric timestamp part
    sorted_short_term_keys = sorted(short_term_memory.keys(), key=lambda k: int(k.split('_')[-1]))

    for key in sorted_short_term_keys:
        text = short_term_memory[key]
        message_entry = None # Initialize message entry

        # Check if the key is a system variant
        if key.startswith("0_system_") or key.startswith("system_"):
                # Create a system message from this entry
                message_entry = {
                    "role": "system",
                    "content": text
                }
                # Note: The '0_' or 'system_' prefix is implicitly handled
                # by just assigning the "system" role and using the value as content.

        else:
                # Process non-system keys (user, assistant, etc.)
                # Extract the role from the key (e.g., "user_123" -> "user")
                # Use split('_', 1) to handle potential underscores within the identifier part
                parts = key.split('_', 1)
                if len(parts) > 0:
                    role = parts[0]
                    # Basic validation for common API roles, excluding 'system' which is handled above
                    valid_roles = ["user", "assistant"]
                    if role in valid_roles:
                            message_entry = {"role": role, "content": text}
                    else:
                        # Handle unexpected roles - maybe default to user?
                        print(f"Warning: Unexpected role '{role}' extracted from key '{key}'. Treating as 'user'.")
                        
                        message_entry = {"role": "user", "content": text}
                else:
                    # Handle keys with no underscore - unexpected, treat as user?
                    print(f"Warning: Key '{key}' in short_term has no underscore. Treating as 'user'.")
                    message_entry = {"role": "user", "content": text}

        # Append the created message entry if one was generated
        if message_entry:
            messages.append(message_entry)


    # print("👾👾 👾👾 THESE ARE THE MESSAGES WE ARE SENDING INTO THE AI 👾👾 👾👾")
    # print(messages)
    return messages
