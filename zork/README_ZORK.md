# frotz Interactive Example: AI with Memory

This example demonstrates the `memory_handle.py`.  Here, we use the memory system to enable an AI to interact with the classic text adventure game **Zork I**. (It should work with any game compatible with Z-code interpreters see [https://ifdb.org] [https://ifdb.org/search?searchbar=z-code])

**What it Does:**

This script (`run_zork.py`) launches Zork I using the `frotz` interpreter and connects it to the AI powered by the `ai_bot` module and the memory management system from `memory_handle.py`.  The AI will:

*   Receive the text output from Zork I.
*   Process this output through the memory system.
*   Generate actions/commands based on its understanding of the game state and memory.
*   Send these commands back to Zork I.

This is **not** intended to be a perfect Zork-solving AI. The primary goal is to showcase how the `memory_handle.py` module can maintain context and influence AI behavior within a turn-based interactive environment like a text adventure game.

**Prerequisites:**

To run this example, you need to install the following and obtain the game data file:

1.  **Frotz Interpreter:**  You need to have `frotz` installed on your system. `frotz` is a popular interpreter for Infocom-style Interactive Fiction games (like Zork). see [https://davidgriffith.gitlab.io/frotz/]

2.  **ZORK1.DAT Game File:** You need to obtain a copy of the game data file for Zork I (typically named ZORK1.DAT, or any other Z-code game) .  **We do not provide this file due to copyright restrictions.**

    *   **Legally Obtaining ZORK1.DAT:**  The most reliable way to obtain `ZORK1.DAT` legally is often through compilations of classic Interactive Fiction games that might be available for purchase or from abandonware sites that host them with permission.  Please ensure you are obtaining the file legally.  Searching online for "ZORK I download legal" might provide some leads, but be cautious about download sources and copyright. 

    *   **Placement:** Once you have `ZORK1.DAT`, you must place it in the **`zork` folder** within the `LLM_Memory_Manager` project directory, alongside the `run_zork.py` script.  So the path should be: `LLM_Memory_Manager/zork/ZORK1.DAT`.

**Running the Zork Example:**

1.  **Navigate to the project root:** Open your terminal and navigate to the main `LLM_Memory_Manager` directory (the one containing `main.py`, `memory_handle.py`, etc.).

2.  **Run the script:** Execute the following command:

    ```bash
    python -m zork.run_zork
    ```

    This command tells Python to run the `run_zork.py` script located in the `zork` subdirectory.

3.  **Observe the AI Playing:** The script will start `frotz` and Zork I. You will see the output from Zork I printed to your terminal, followed by the "Zork says:" prefix. Then, you will see the AI's "Thoughts" and the "Action" (command) it decides to send to the game.

    The AI will then interact with Zork I automatically. Observe how the AI explores the game world and responds to the game's descriptions.

**Important Notes:**

*   **Experimental and Demonstrative:** This Zork example is experimental and primarily for demonstration purposes.  Do not expect it to be a highly intelligent or optimal Zork player.  It's designed to showcase the memory system, not advanced game AI.
*   **Memory in Zork:** The memory system will attempt to remember aspects of the game, such as:
    *   Game descriptions provided by Zork.
    *   Actions taken by the AI.
    *   Potentially key objects or locations mentioned.
    *   This memory is then used to inform the AI's subsequent actions.
*   **Patience Required:** Give the script a moment to initialize when you first run it. There might be a slight delay as Frotz starts and the AI processes the initial game text.
*   **Customization:** You can adjust the AI's persona and behavior by modifying the system prompt in the `run_zork.py` script, just as with the CLI chatbot.

**Directory Structure (within `LLM_Memory_Manager`):**

zork/
├── run.py <- The Zork example script
├── ZORK1.DAT <- (You need to place this here)
└── README_ZORK.md <- This file




We hope this Zork I example provides a more concrete and engaging way to understand the functionality of the `memory_handle.py` module within an interactive context.
