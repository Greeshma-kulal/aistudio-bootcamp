# Day 4 – LLM API Chatbot

## Overview
A command-line chatbot built using the OpenRouter API and Python. It supports streaming responses, maintains conversation history, tracks token usage, and logs API usage information.

## Features
- Interactive command-line chatbot
- Streaming LLM responses
- Conversation history
- Token usage tracking
- API usage and estimated cost logging
- Retry handling for HTTP 429 and 5xx errors

## Technologies Used
- Python 3.12
- OpenAI Python SDK
- OpenRouter API
- python-dotenv
- Tenacity

## Project Structure
```text
day-04-llm-chatbot/
├── chat.py
├── requirements.txt
├── cost_log.csv
├── .env
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Create a `.env` file and add your OpenRouter API key:

   `OPENROUTER_API_KEY=your_api_key`

4. Run the chatbot:

   `python chat.py`

## Usage
Enter a message to chat with the model. Type `exit` to end the conversation.

Token usage and available cost information are recorded in `cost_log.csv`.

## Security
Never commit `.env` or expose API keys. The virtual environment should not be committed to Git.