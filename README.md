# AI Agent

This repository contains the code for an AI assistant that can help users with different tasks by generating specific actions based on their inputs and context. The AI assistant uses OpenAI's GPT-3 model to generate text, and can perform tasks such as searching the web, browsing websites, asking for information, and providing final answers.

The main files in the repository are:

- `app.py`: This is the main script that runs the AI assistant. It imports the `kernel` module and uses the `CompletionAgent` class to generate actions based on user inputs and context.
- `kernel/__init__.py`: This file exports some of the key modules for the AI assistant, including `CompletionAgent`, `ChatAgent`, `Config`, and `web`.
- `kernel/config.py`: This file defines the `Config` class, which holds the configuration settings for the AI assistant, such as the OpenAI API key, the model to use, and the maximum number of tokens to generate.
- `kernel/agent.py`: This file defines the `Agent` base class and its derived classes `CompletionAgent` and `ChatAgent`, which provide different functionalities for the AI assistant, such as generating completions and holding conversation with users.
- `kernel/actions/web.py`: This file provides some utility functions for web scraping and browsing, such as searching Google and getting web pages.

To use the AI assistant, you need to have an OpenAI API key and set it as an environment variable named `OPENAI_API_KEY`. Then you can run the `app.py` script and enter some input text to get the AI assistant's response. The AI assistant will generate an action based on the input text and print it out, along with any additional context or prompts needed to perform the action. The AI assistant can also hold a conversation with users using the `ChatAgent` class.

Enjoy using the AI assistant!

##### Generated using DocaAI