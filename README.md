# AI Agent

This repo contains a collection of Python modules and scripts for building a conversational agent that can generate actions to address user needs and perform web-based actions including web browsing, information retrieval, and searching.

The following libraries are required to run this app:

- openai
- tiktoken
- requests
- bs4 (Beautiful Soup)
- python-dotenv

Here is an overview of each module in the codebase:

- `app.py`: The main script that runs the conversational agent. It imports `kernel`, `os`, `re`, `BeautifulSoup`, and `load_dotenv` from the `dotenv` module. It creates an instance of the `CompletionAgent` class defined in `kernel/agents/agent.py` and listens for user input. Based on the generated actions, it performs various web actions including web browsing and information retrieval.
- `kernel/__init__.py`: Initializes the package and imports symbols from other modules.
- `kernel/agents/config.py`: Defines the `Config` class for holding configuration settings for an agent, such as the OpenAI API key, system prompt, and model parameters.
- `kernel/agents/agent.py`: Contains the base `Agent` class and two subclasses: `CompletionAgent` and `ChatAgent`. These classes define how the agent communicates with OpenAI's GPT models and handles context. They also use external libraries such as `tiktoken` for tokenizing the input text.
- `kernel/actions/web.py`: Contains functions for performing web actions (e.g. web browsing and searching).
- `kernel/__init__.py`: For exporting the functions in `kernel/actions/web.py`.

To run the app, ensure that you have installed all the required libraries and set the `OPENAI_API_KEY` environment variable to your API key. Then run the `app.py` script.

Enjoy using the AI assistant!

##### Generated using DocaAI