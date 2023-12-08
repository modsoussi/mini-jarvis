# Mini-Jarvis

An AI agent that uses the GPT model to generate actions in order to achieve a given goal. It can perform complex actions such as browsing, clicking, input filling, and asking for additional information.

## Features

- Utilizes GPT model to generate conversational responses.
- Performs browsing activity.
- Searches on Google.
- Can click on UI elements within a webpage.
- Fills out form inputs on pages.
- Asks for extra information from users when needed.

## Installation

### Pip

Create a virtual environment and activate it:

```shell
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Clone the repository and navigate to the project directory:

```shell
git clone https://github.com/modsoussi/mini-jarvis
cd mini-jarvis
```

Then, install the required packages:

```shell
pip install -r pip.env
```

### Conda

First, clone the repository:

```shell
git clone https://github.com/modsoussi/mini-jarvis
```

Then, create and activate a Conda environment:

```shell
conda create -n myenv -f conda.env
conda activate myenv
```

Navigate to the project directory:

```shell
cd mini-jarvis
```

## Set Up

Create a .env file and add the OpenAI API key.

```shell
OPENAI_API_KEY="YOUR_OPEN_AI_API_KEY"
```

## Usage

Before running, make sure to activate your Python environment:

For pip

```shell
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

For conda

```shell
conda activate myenv
```

Then run the kernel with:

```shell
python app.py
```

Some things you can ask MiniJarvis to do:
- What are the top 5 posts on Hacker News today?
- Summarize the comments on the top post on Hacker News
- Find me Airbnb engineering openings in Paris, France

## License

This project is licensed under the terms of the MIT license.