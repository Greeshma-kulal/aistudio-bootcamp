# Day 5 – Structured Equipment Complaint Triager

## Overview
A command-line hospital equipment complaint triage application
using an LLM, OpenRouter function calling, and Pydantic validation.

## Features
- Structured complaint classification
- Function calling for structured model output
- Pydantic validation
- One retry for invalid model output
- Prompt versioning (v1 and v2)
- Few-shot prompting
- Basic prompt-injection protection
- Evaluation using 20 synthetic complaints
- CSV accuracy report

## Output Fields
- equipment
- urgency
- hospital
- next_action

## Technologies
- Python 3.12
- OpenRouter API
- OpenAI Python SDK
- Pydantic
- python-dotenv

## Setup

Install dependencies:

    pip install -r requirements.txt

Add your OpenRouter API key to `.env`:

    OPENROUTER_API_KEY=your_api_key
    OPENROUTER_MODEL=openrouter/free

## Run the CLI

    python triager.py

Choose v1 or v2 and enter a complaint.

## Run Evaluation

    python evaluate.py

The script evaluates both prompts against 20 synthetic samples
and generates `accuracy.csv`.

## Security
Never commit `.env` or expose API keys.
The complaint text is treated as untrusted input.