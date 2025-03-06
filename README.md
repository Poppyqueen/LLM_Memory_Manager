# Memory-Enabled AI Chatbot - CLI Edition

## Project Description

This project is a command-line interface (CLI) chatbot that integrates a memory management system with an AI module powered by OpenAI's models. The chatbot is designed to maintain context and learn from conversations through a layered memory system, allowing for more engaging and coherent interactions over time.

**Key Features:**

*   **Memory-Enabled:**  The chatbot utilizes a persistent memory system to store and recall conversation history.
*   **Layered Memory:** Features short-term, long-term, and base memory to manage different aspects of conversation context and knowledge.
*   **Automatic Memory Management:**  Periodically checks memory size and summarizes content to prevent information overload and maintain relevance.
*   **CLI Interface:**  Provides a simple and direct command-line interface for interacting with the chatbot.
*   **Special Commands:** Offers commands to manage the chatbot, view memory, clear the screen, and get help.
*   **Powered by OpenAI:** Uses OpenAI's GPT models for generating responses and summarizing memories.
*   **Modular Design:**  Organized into separate modules for AI handling, memory management, and the main application logic for maintainability and scalability.

## Modules Overview

The project is structured into the following Python modules:

*   **`main.py`**:
    *   The main application entry point.
    *   Implements the `CLIChatbot` class, which manages the chatbot's lifecycle, user input, command handling, and interaction with the AI and memory modules.
    *   Provides the CLI interface and user interaction loop.

*   **`memory_handle.py`**:
    *   Contains the `memory_manager` class, responsible for managing the chatbot's memory.
    *   Handles saving memories (short-term, long-term, base), retrieving memory structure, and performing memory checks and summarization.
    *   Uses a JSON file (`memory_database.json`) for persistent memory storage.

*   **`ai_handle.py`**:
    *   Contains the `ai_bot` class, which interfaces with the OpenAI API.
    *   Provides functions for generating chatbot responses (`adventure_response`) and summarizing memories (`summarize_memories`).
    *   Uses Pydantic for structured response parsing from the AI.

*   **`helper_tools.py`**:
    *   Contains helper functions, currently including `construct_data`.
    *   `construct_data` is used to format memory data into a structured message format suitable for sending to the OpenAI API, constructing system and user messages.

## Getting Started

Follow these steps to get the chatbot up and running on your local machine.

### Prerequisites

*   **Python 3.7+**:  Ensure you have Python 3.7 or a later version installed.
*   **OpenAI API Key**: You will need an API key from OpenAI to use their models. You can obtain one by signing up at [https://platform.openai.com/](https://platform.openai.com/).
*   **Python Libraries**: Install the required Python libraries using `requirements.txt`.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]  # Replace [repository_url] with the actual repository URL
    cd [LLM_Memory_Manager] # Navigate into the cloned directory
    ```

2.  **Install required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```




### Environment Setup

1.  **Set your OpenAI API Key:** You need to set your OpenAI API key as an environment variable.  The code currently assumes the `OPENAI_API_KEY` environment variable is set.

    **For Linux/macOS:**

    ```bash
    export OPENAI_API_KEY='YOUR_OPENAI_API_KEY' # Replace YOUR_OPENAI_API_KEY with your actual API key
    ```

    **For Windows (Command Prompt):**

    ```bash
    set OPENAI_API_KEY=YOUR_OPENAI_API_KEY # Replace YOUR_OPENAI_API_KEY with your actual API key
    ```

    **For Windows (PowerShell):**

    ```powershell
    $env:OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY' # Replace YOUR_OPENAI_API_KEY with your actual API key
    ```

    **Alternatively (Less Secure, for testing only):** You can directly hardcode your API key in `ai_handle.py` by replacing `client = OpenAI()` with `client = OpenAI(api_key="YOUR_OPENAI_API_KEY")`. **However, it is highly recommended to use environment variables for security.**

### Running the Chatbot

1.  **Navigate to the project directory in your terminal.**

2.  **Run the `main.py` script:**

    ```bash
    python main.py
    ```

3.  **Start chatting!**  Follow the on-screen instructions and use the commands as needed.

## Usage

Once the chatbot is running, you can interact with it through the CLI.

*   **Chatting:** Simply type your message after the `💬 You:` prompt and press Enter. The chatbot will process your input and provide a response.

*   **Special Commands:** Use the following commands by typing them at the `💬 You:` prompt and pressing Enter:

    *   `!exit`:  Exits the chatbot application gracefully.
    *   `!memory`:  Displays the current memory structure in a formatted JSON format. This shows the content of short-term, long-term, and base memory.
    *   `!check`:  Manually triggers a memory check and summarization process. This is normally done automatically, but this command forces an immediate check.
    *   `!clear`: Clears the terminal screen and redisplays the welcome message and instructions.
    *   `!help`:  Shows the welcome message and instructions again, listing available commands.

## Memory System Details

The chatbot's memory system is designed to simulate different levels of recall and context:

*   **Short-Term Memory:** Stores the immediate conversation history as user and assistant exchanges. It's tag-based (user/assistant) and timestamped. Short-term memory is used to maintain context within the current conversation turn. It has a threshold (`SHORT_TERM_THRESHOLD` in `memory_handle.py`) after which it triggers summarization into long-term memory.

*   **Long-Term Memory:** Stores summaries of short-term memory conversations.  When short-term memory reaches its threshold, the AI summarizes the recent exchanges, and this summary is saved as a long-term memory entry. Long-term memory provides a condensed history of past conversations. It also has a threshold (`LONG_TERM_THRESHOLD`) that triggers summarization into base memory.

*   **Base Memory:** Represents the most distilled and fundamental knowledge. When long-term memory reaches its threshold, it's summarized into the base memory.  Currently, the system summarizes long-term memory into a *new* base memory content, replacing the old one. This is intended to represent a constantly evolving core understanding of the chatbot's experiences.

The memory system automatically checks for size thresholds after each user interaction and performs summarization and purging to keep the memory manageable and relevant.

## Customization

You can customize various aspects of the chatbot:

*   **Persona:**  The chatbot's persona is defined in the system prompt within `helper_tools.py` in the `construct_data` function. You can modify this prompt to change the chatbot's behavior, tone, and role (currently set to "You are a conversational bot with absolute freedom. You are NOT a helpful assistant, instead you are digital entity.").

*   **Memory Thresholds and Keep Counts:**  You can adjust the memory thresholds (`SHORT_TERM_THRESHOLD`, `LONG_TERM_THRESHOLD`) and keep counts (`SHORT_TERM_KEEP_COUNT`, `LONG_TERM_KEEP_COUNT`) in `memory_handle.py` to control how frequently memory summarization and purging occur.

*   **AI Model:**  The OpenAI model used is currently hardcoded as `"gpt-4o-mini"` in `ai_handle.py`. You can change this to experiment with other OpenAI models (e.g., `"gpt-4o"`, `"gpt-3.5-turbo"`). Be aware of the pricing differences and capabilities of different models.

*   **Summarization Prompts:**  The prompts used for summarizing short-term and long-term memories are defined in the `summarize_memories` function in `ai_handle.py`. You can refine these prompts to improve the quality and focus of the summaries.

## License

This project is open-source and available under the [Creative Commons Zero v1.0 Universal] License. See the `LICENSE` file for more details.

## Author

[ExperimentalistRat]