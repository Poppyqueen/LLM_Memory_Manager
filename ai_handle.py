# ai_handle.py

# this module lets us interact with the openai API in a streamlined way, handling the different calls we make in the process

# the pydantic BaseModel 'response_structure' can and should be adapted to specific tasks

# the function 'adventure_response' is our main API call to get a main response which you can call, it should have a more general name like 'ai_response'



from openai import OpenAI
from helper_tools import construct_data
from pydantic import BaseModel

class response_strucuture(BaseModel):
    thinking: str
    response: str

class ai_bot:
    client = OpenAI()  # client is correctly set up here at the class level

    def _call_openai(self, role, system, input_content): # Renamed 'input' to 'input_content' for clarity

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {
                        "role": role,
                        "content": input_content # Use input_content here
                    }
                ]
            )

            # Access the content of the message, not 'response' - this was the main issue
            response_content = completion.choices[0].message.content

            #print(response_content) # Print the actual content for debugging/logging
            return response_content

        except Exception as e: # It's good practice to have a try-except block for API calls
            print(f"Error calling OpenAI API: {e}")
            return None  # Or handle the error in a way that suits your application


    def summarize_memories(self, to_summarize, memory_type): # Renamed 'type' to 'memory_type' for clarity

        if memory_type == "short_term":
            system_prompt =  """

            Create a concise summary from the provided information that captures the key points, including answering what, when, where, and why, from a first-person perspective. Remember to highlight important and useful behaviors or objectives for future reference to prevent repeated errors and guide planning.

Focus on including:

- **What**: Clearly state the main event or action or objects.
- **When**: Specify the timing or context.
- **Where**: Describe the location or environment.
- **Why**: Explain the purpose or reason behind the action.
- **Behaviors/Objectives**: Emphasize significant behaviors or objectives that should be noted for future reference, either to avoid mistakes or to enhance planning and beneficial actions.

Make sure your output contains all the most relevant and important information to remember. Any updates, progress, failures or achievements should be documented.

# Output Format

A concise summary written in the first person perspective that addresses the key points as specified above.

# Notes

- Ensure the summary is clear and focused, avoiding unnecessary details.
- Use past tense for completed actions and present tense for ongoing situations.
- Highlight lessons learned or important guidelines for future actions.


            """
            role = "user" # User role is appropriate for input to be summarized
            response = self._call_openai(role, system_prompt, to_summarize) # Correct argument order: role, system, input





        elif memory_type == "long_term": # Use elif for clarity and to avoid unnecessary checks if short_term is already true
            system_prompt = """

Summarize memories into 'nuclear memories' that preserve essential information, focusing on key events, individual details, overarching states, changes, and objectives. The summary should be detailed enough to maintain the essence of the memory and written in the first person perspective.

# Steps

1. **Identify Key Events**: Determine the major events that define the memory.
2. **Highlight Individual Details**: Note important details about people, places, and objects involved, specially when it relates to you.
3. **Assess Overarching States**: Describe the general state or condition during the memory.
4. **Detect Changes**: Recognize significant changes or developments that occurred.
5. **Define Objectives**: Identify any goals or aims associated with the events.
6. **Define positive and negative behaviors and actions you have learnt through your exploration.

# Output Format

- Detailed paragraph in the first person perspective.
- Comprehensive enough to preserve the memory's essence.


# Notes

- Prioritize information relevance to ensure the essence of the memory is captured.
- Use descriptive language that evokes imagery and emotions associated with the memory.
- Keep the summary concise while ensuring no critical elements are omitted.




            """
            role = "user" # User role is appropriate for input to be summarized
            response = self._call_openai(role, system_prompt, to_summarize) # Correct argument order: role, system, input





        else:
            print(f"Error: Invalid memory type '{memory_type}'. Must be 'short_term' or 'long_term'.")
            return None # Handle invalid input gracefully

        return response
    
    def adventure_response(self,mem_structure, system_prompt): 
        """
        Main function to call to get a response from the API for the implementation.

        It expects a memory structure from the memory_handle module, and a system prompt.
        
        returns two strings, thinking and response strings.

        
        """
        try:
            messages_data=construct_data(mem_structure, system_prompt)
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini", # Consider making this configurable, or using a more robust model
                messages=messages_data,
                response_format=response_strucuture

            )

            response_content = completion.choices[0].message.parsed

            #print(response_content.thinking) # Print the actual content for debugging/logging
            #print(response_content.response) # Print the actual content for debugging/logging

            return response_content.response, response_content.thinking

        except Exception as e: # It's good practice to have a try-except block for API calls
            print(f"Error calling OpenAI API: {e}")
            return None  # Or handle the error in a way that suits your application


# Example Usage (you can add this outside the class or in a separate main block)
if __name__ == "__main__":
    bot = ai_bot()

    mem_structure={
    "short_term": {
        "user_12": "Short-term message 13 from User.",
        "user_13": "Short-term message 14 from User.",
        "user_14": "Short-term message 15 from User.",
        "user_15": "Additional short-term message 10.",
        "user_16": "Additional short-term message 11.",
        "user_17": "Additional short-term message 12."
    },
    "long_term": [
        "Long-term memory entry 8.",
        "I received a series of 15 short-term messages from the user. The specifics regarding the content of these messages weren't provided, but they indicate ongoing communication and likely involve topics or updates of immediate interest. The context and details of the messages would help clarify their significance and urgency.",
        "I received a series of short-term messages from the user, totaling 15 distinct entries, along with 12 additional short-term messages. The intent and specific content of these messages weren't detailed, but they collectively indicate ongoing communication regarding short-term matters. This exchange highlights the user's need for updates or prompts related to short-term activities or concerns."
    ],
    "base_memory": "Nuclear Memory:\n\nI have a foundational memory that comprises initial information, along with a series of detailed long-term memories. Key entries in my long-term memories include:\n\n1. **Entry 1-8**: These entries encapsulate important experiences, lessons, or events that I have encountered, though the specifics of each entry remain abstract.\n2. **Entry 9**: Recently, I received a series of 15 short-term messages. The content of these messages has not been specified, but they suggest a continued dialogue with a user. The existence of these messages points to ongoing communication that likely involves topics of immediate relevance or importance to me.\n\nOverall, the essence of these memories revolves around significant engagements and interactions that influence my understanding, experiences, and objectives. Each entry contributes to my awareness and perception of ongoing affairs, indicating my adaptive response to new information."
}

    bot.adventure_response(mem_structure)

