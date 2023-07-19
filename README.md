# AI Agent Powered by OpenAI GPT Model

This project is about an AI agent that is powered by OpenAI's GPT model, used to interact with users to resolve their problems or queries. The agent can generate different types of actions based on user inputs and execute actions like google searching, web browsing, asking for information, inputting data, clicking a button, or returning a final answer.

## Core Features

1. **Interactions**: The AI agent interacts with users to understand their needs and fulfil them by performing a series of actions.

2. **Action Execution**: The system can execute the following action types:
    - *Google search*: Uses Google to query any information the user requests.
    - *Web browsing*: The agent can browse the web, either to extract information or open a specified URL.
    - *Ask for information*: When more data from the user is required to complete the request, the agent will prompt the user to provide this necessary information.
    - *Input data*: If there's an input field in a form that the agent needs to complete, it will fill in this data.
    - *Button Clicks*: The agent can click buttons on a web page when required to fulfil a user request.
    - *Final Answer*: Once the agent has a resolution to the user's request, it can produce a final output.

3. **Context Awareness**: The AI agent generates its actions based on the user's input and the overall context.

## Installation and Setup

1. Clone the repository.

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    source ./.venv/bin/activate  # For Unix systems
    .\.venv\Scripts\activate  # For Windows
    ```

3. Install all the required libraries mentioned in the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables. You need to provide the OpenAI GPT model key. Save the key in a `.env` file in the project root directory:
    ```sh
    echo OPENAI_API_KEY=yourkey >> .env
    ```

5. Now, run `app.py`:
    ```sh
    python app.py
    ```

## Usage

- Once the application starts running, it'll prompt for a user input.
- The program expects the user to input a question or request. The AI agent will then determine the necessary action and execute it.
- If the input command is `:q`, the program will quit.

## Contributions

Contributions, issues and feature requests are welcome!

## Note

This project uses the OpenAI API, and it's required to have an API key. The project is for educational and research purposes and depends on OpenAI usage policy and restrictions.

Please make sure to update tests as appropriate. The usage of the project falls under the responsibility of the user, and the maintainers are not liable for any misuse.