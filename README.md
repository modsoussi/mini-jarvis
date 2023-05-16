# Mini-Jarvis

Mini-Jarvis is a Python-based AI assistant that can answer questions and perform actions, using the OpenAI API and several Python packages including `requests`, `bs4`, and `dotenv`.

## Installation

In order to use Mini-Jarvis, you will need to set up a virtual environment and install the required Python packages. Here are the steps to do this:

1. Clone this repository to your local machine.

2. Navigate to the root directory of the repository in your terminal and run the following command to create a virtual environment:
```
python3 -m venv venv
```
3. Activate the virtual environment by running:
```
source venv/bin/activate
```
4. Install the required packages by running:
```
pip install -r requirements.txt
```
5. Set up your OpenAI API key by creating a `.env` file in the root directory of the repository, and adding the following line (with your actual API key):
```
OPENAI_API_KEY=<your API key here>
```

## Usage

Once you have installed Mini-Jarvis, you can use it to ask questions and perform actions. Here's how to do this:

1. Go to the root directory of the repository in your terminal.
2. Activate the virtual environment by running:
```
source venv/bin/activate
```
3. Run the `app.py` file by running:
```
python app.py
```
4. You should see a prompt that says `>> `. Enter a question or request.
5. Mini-Jarvis will process your input and generate an action to perform. You may see a `[google-search]` instruction, for example. Follow the instructions to provide the information Mini-Jarvis needs to complete the action.
6. Mini-Jarvis will return the results of the action, and may generate additional instructions or prompts for more information.
7. Continue interacting with Mini-Jarvis until you have received the answer or action you were looking for.

##### Generated using DocaAI