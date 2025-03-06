# memory_handle.py
# Memory handle is a module to manage memory storage for an LLM, the system can be integrated into various situations where an agent needs
# to maintain a constant memory.

# It helps you set up a JSON database, to do different kinds of querries for memory management, the memory manager class contains functions to save
# memories into different sections and engage in a 'check' to summarize memories above our thesholds.


import json
import os

class memory_manager:

    # These numbers need to be adjusted to find an optimal spot, only having tried gpt-4o-mini, lower is better, maybe half of what it is now is best for coherence during conversation and summarization.
    SHORT_TERM_THRESHOLD = 30  # Number of short-term entries before summarizing
    LONG_TERM_THRESHOLD = 20   # Number of long-term entries before summarizing
    SHORT_TERM_KEEP_COUNT = 10  # Number of latest short-term entries to keep after summarizing
    LONG_TERM_KEEP_COUNT = 10   # Number of latest long-term entries to keep after summarizing

    def __init__(self, ai_bot_instance=None, filepath="memory_database.json"):
        """
        Initializes the memory manager with the path to the JSON database file
        and an optional AI bot instance.
        """
        self.filepath = filepath  # Now filepath is configurable
        self._check_and_create_db()

        # Use provided bot instance or create a new one if needed
        if ai_bot_instance:
            self.bot_instance = ai_bot_instance
        else:
            from ai_handle import ai_bot
            self.bot_instance = ai_bot()

    def _check_and_create_db(self):
        """
        Internal function to check if the JSON database file exists and create it if not.
        """
        if not os.path.exists(self.filepath):
            initial_memory = {
                "short_term": {},
                "long_term": [],
                "base_memory": ""
            }
            with open(self.filepath, 'w') as f:
                json.dump(initial_memory, f, indent=4)
            print(f"Database file created at: {self.filepath}")

    def _load_memory(self):
        """
        Internal function to load memory data from the JSON file.
        """
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Database file not found at {self.filepath}. Please check the path.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.filepath}. File might be corrupted.")
            return None

    def _save_memory(self, memory_data):
        """
        Internal function to save memory data to the JSON file.
        """
        try:
            with open(self.filepath, 'w') as f:
                json.dump(memory_data, f, indent=4)
        except Exception as e:
            print(f"Error saving to database file: {e}")



    def save_to_memory(self, string_to_save, memory_type, tag=None):
        """Saves a string to the specified memory section.

        It expects a string to save.\n
        The memory type, (short term, long term or base).\n
        A tag for the sender of the message, (only necesary for short term memories).\n\n\n



        If you want to add memories, the recommended memory type to use when accesing this in your project is 'short_term'.
        For the identity tag use 'user' and 'assistant'.

        Unless you want to get experimental, do not change this.


        """
        memory_data = self._load_memory()
        if memory_data is None:
            return

        memory_type = memory_type.lower()
        import time
        current_time = int(time.time())

        if memory_type == "short_term":
            if tag is None:
                print("Error: Tag is required for short_term memory.")
                return

            # Use tag directly without appending numbers
            tag = tag.lower()

            formatted_time = time.ctime(current_time)

            string_to_save = f"Time of the exchange: {formatted_time}\n Exchange: {string_to_save}"

            # Get the current short-term memory entries
            short_term_memory = memory_data.get("short_term", {})

            # Create a unique key using the tag and timestamp
            key = f"{tag}_{current_time}"
            short_term_memory[key] = string_to_save
            memory_data["short_term"] = short_term_memory

        elif memory_type == "long_term":
            print("Attempting to save a long term memory!")

            # Get current long-term memory list
            long_term_memory = memory_data.get("long_term", [])

            # Format the timestamp as a human-readable date/time
            from datetime import datetime
            timestamp_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

            # Combine timestamp and memory content into a single string
            formatted_memory = f"[{timestamp_str}] {string_to_save}"

            # Append the formatted string to the long-term memory list
            long_term_memory.append(formatted_memory)
            memory_data["long_term"] = long_term_memory

            print("Long term memory saved!")

        elif memory_type == "base_memory":
            memory_data["base_memory"] = string_to_save

        else:
            print(f"Error: Invalid memory_type '{memory_type}'.")
            return

        self._save_memory(memory_data)
        # print(f"Saved to '{memory_type}' memory: '{string_to_save}'") # we want to be logigng this too



    def get_memory_structure(self, formatted=False):
        """
        Retrieves and returns the current memory structure.

        Args:
            formatted (bool, optional): If True, returns a formatted string representation
                                        of the memory structure for better readability.
                                        If False (default), returns the raw memory data as a dictionary.

        Returns:
            dict or str: The memory structure. Returns a dictionary by default,
                         or a formatted string if formatted=True.
        """
        memory_data = self._load_memory()
        if formatted:
            return json.dumps(memory_data, indent=4) # Return formatted JSON string
        else:
            return memory_data # Return raw dictionary




    def check(self):
        """
        Checks memory lengths, summarizes if thresholds are reached, and purges old memories.
        """
        memory_data = self._load_memory()
        if memory_data is None:
            return

        # --- Short-Term Memory Check ---
        short_term_memory = memory_data.get("short_term", {})
        if len(short_term_memory) >= self.SHORT_TERM_THRESHOLD:
            print("\n--- Short-Term Memory Check Triggered ---")
            structured_short_term = ""

            # Sort keys by timestamp (newest last)
            # Keys are in format "tag_timestamp" so splitting and getting the timestamp part
            sorted_short_term_keys = sorted(short_term_memory.keys(),
                                        key=lambda k: int(k.split('_')[1]))

            for key in sorted_short_term_keys:
                tag = key.split('_')[0].capitalize() # Extract tag from key
                structured_short_term += f"[{tag}]: {short_term_memory[key]}\n"

            if structured_short_term: # Only call AI if there's something to summarize
                print("DEBUG: Creating short-term summary")
                # Assuming ai_bot_instance is defined and has summarize_memories method
                summary_short_term = self.bot_instance.summarize_memories(structured_short_term, "short_term")
                print(f"DEBUG: Summary created: {summary_short_term[:50]}...")  # Print first 50 chars

                # Use save_to_memory instead of directly modifying the data structure
                self.save_to_memory(summary_short_term, "long_term")
                print("DEBUG: Summary saved to long-term memory")

                # Reload memory data after saving the summary
                memory_data = self._load_memory()

                # Purge oldest short-term memories, keep latest SHORT_TERM_KEEP_COUNT
                # Take the keys from the end of the sorted list (newest ones)
                keys_to_keep = sorted_short_term_keys[-self.SHORT_TERM_KEEP_COUNT:]
                new_short_term = {key: short_term_memory[key] for key in keys_to_keep}

                # Use a temporary dictionary to update short_term
                temp_memory = memory_data.copy()
                temp_memory["short_term"] = new_short_term
                self._save_memory(temp_memory)

                print(f"Short-term memory purged, keeping latest {self.SHORT_TERM_KEEP_COUNT} entries.")

        # --- Long-Term Memory Check ---
        # Reload memory to ensure we're working with the latest data including any short-term summaries
        memory_data = self._load_memory()
        long_term_memory = memory_data.get("long_term", [])

        if len(long_term_memory) >= self.LONG_TERM_THRESHOLD:
            print("\n--- Long-Term Memory Check Triggered ---")
            structured_long_term = ""

            for i, entry in enumerate(long_term_memory):
                if isinstance(entry, dict) and "memory" in entry:
                    entry_text = entry["memory"]
                else:
                    entry_text = str(entry)
                structured_long_term += f"[Entry {i+1}]: {entry_text}\n"

            base_memory_content = memory_data.get("base_memory", "")
            structured_for_ai = f"Base Memory:\n{base_memory_content}\n\nLong-Term Memories:\n{structured_long_term}"

            if structured_for_ai: # Only call AI if there's something to summarize
                print("DEBUG: Creating long-term summary")
                summary_long_term_base = self.bot_instance.summarize_memories(structured_for_ai, "long_term")
                print(f"DEBUG: Base memory summary created: {summary_long_term_base[:50]}...")

                # Use save_to_memory for base memory too
                self.save_to_memory(summary_long_term_base, "base_memory")
                print("DEBUG: Summary saved to base memory")

                # Reload memory to get the latest state
                memory_data = self._load_memory()
                long_term_memory = memory_data.get("long_term", [])

                # Keep only the latest entries
                if len(long_term_memory) > self.LONG_TERM_KEEP_COUNT:
                    entries_to_keep = long_term_memory[-self.LONG_TERM_KEEP_COUNT:]

                    # Clear the long-term memory first
                    temp_memory = memory_data.copy()
                    temp_memory["long_term"] = []
                    self._save_memory(temp_memory)

                    # Re-add each entry using save_to_memory
                    for entry in entries_to_keep:
                        if isinstance(entry, dict) and "memory" in entry:
                            self.save_to_memory(entry["memory"], "long_term")
                        else:
                            self.save_to_memory(str(entry), "long_term")

                    print(f"Long-term memory purged, keeping latest {self.LONG_TERM_KEEP_COUNT} entries.")

        print("\n--- Memory Check Completed ---")

# Example Usage (with check function):
if __name__ == "__main__":
    # Example 1: Using default filepath "memory_database.json"
    memory_system_default = memory_manager()

    # Example 2: Using a custom filepath "my_custom_memory.json"
    memory_system_custom = memory_manager(filepath="my_custom_memory.json")

    print("\n--- Default Memory System - Filepath:", memory_system_default.filepath, "---")
    print("\n--- Custom Memory System - Filepath:", memory_system_custom.filepath, "---")

    # You can now use memory_system_default and memory_system_custom independently,
    # each will use its own database file.

    # Let's work with the default one for the rest of the example as before

    # Fill up short-term memory to trigger check
    for i in range(15):
        memory_system_default.save_to_memory(f"Short-term message {i+1} from User.", "short_term", "user")

    # Fill up long-term memory to trigger check
    for i in range(8):
        memory_system_default.save_to_memory(f"Long-term memory entry {i+1}.", "long_term")

    memory_system_default.save_to_memory("Initial base memory content.", "base_memory")

    print("\n--- Memory Structure Before Check (Raw) ---")
    print(memory_system_default.get_memory_structure()) # Raw dictionary

    print("\n--- Memory Structure Before Check (Formatted) ---")
    print(memory_system_default.get_memory_structure(formatted=True)) # Formatted JSON string

    memory_system_default.check()  # Run the memory check and summarization

    print("\n--- Memory Structure After Check (Formatted) ---")
    print(memory_system_default.get_memory_structure(formatted=True)) # Formatted JSON string

    # Add more short-term memories to trigger another check
    print("\n--- Adding More Short-Term Memories ---")
    for i in range(12):
        memory_system_default.save_to_memory(f"Additional short-term message {i+1}.", "short_term", "user")

    print("\n--- Running Second Memory Check ---")
    memory_system_default.check()

    print("\n--- Final Memory Structure (Formatted) ---")
    print(memory_system_default.get_memory_structure(formatted=True)) # Formatted JSON string
