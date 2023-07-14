# Mini-Jarvis

Mini-Jarvis is a Python repository that implements a basic AI assistant called MARKI. It utilizes the OpenAI GPT-3 language model to generate contextual actions and responses based on user input and system prompts.

## Getting Started

To get started with Mini-Jarvis, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/mini-jarvis.git`
2. Install the required dependencies listed in the `requirements.txt` file: `pip install -r requirements.txt`
3. Replace the placeholder OpenAI API key in the `app.py` file with your own API key.
4. Run the application: `python app.py`

## Files

The repository consists of the following files:

- `app.py`: The main Python script that runs the Mini-Jarvis AI assistant. It imports the necessary modules and sets up the configuration for the assistant.
- `sys.py`: Contains the system prompt instructions for Mini-Jarvis. These instructions define the behavior and types of actions the assistant can generate.
- `kernel` (directory):
  - `agents` (directory):
    - `agent.py`: Contains the `Agent` base class and its subclasses `CompletionAgent` and `ChatAgent`, which handle the interaction with the OpenAI language model.
    - `config.py`: Defines the `Config` class, which holds the configuration settings for the agents.
    - `__init__.py`: Initializes the agents package.
  - `actions` (directory):
    - `action.py`: Implements the `Action` class, which represents an action that Mini-Jarvis can take. It includes methods for executing the action and generating a description of the action.
    - `__init__.py`: Initializes the actions package.
  - `browser.py`: Provides a `Browser` class that handles web browsing functionality for Mini-Jarvis, such as opening pages, filling out forms, and performing Google searches.
  - `__init__.py`: Initializes the kernel package.
- `parser.py`: Implements a parser class that extracts relevant information from HTML content.
- `__init__.py`: Initializes the mini-jarvis package.
- `__main__.py`: Provides a command-line interface for manually browsing web content using the `Browser` class.

## Usage

When running the Mini-Jarvis AI assistant, it will prompt you to enter a question or command. You can interact with Mini-Jarvis by entering text input. The assistant will generate actions and responses based on the given input and its context.

Mini-Jarvis can perform various types of actions, including Google searches, web browsing, form filling, and more. The generated actions will be displayed, and the assistant will execute them accordingly.

To exit Mini-Jarvis, simply enter `:q` in the input prompt.

## Contributing

Contributions to Mini-Jarvis are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

Mini-Jarvis is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for your own purposes.

## Acknowledgements

Mini-Jarvis is built upon the OpenAI GPT-3 language model and uses various open-source libraries, which are listed in the `requirements.txt` file. Special thanks to the developers and contributors of those libraries.

## Disclaimer

Mini-Jarvis is a proof-of-concept AI assistant and should not be used for sensitive or critical tasks. Use at your own risk.