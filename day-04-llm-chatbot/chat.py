
import os
import csv
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI, APIStatusError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception,
    before_sleep_log
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

# Initialize OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    max_retries=0
)

MODEL = "openrouter/free"

# CSV cost log
LOG_FILE = Path(__file__).resolve().parent / "cost_log.csv"

if not LOG_FILE.exists():
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "model",
            "input_tokens",
            "output_tokens",
            "estimated_cost_usd"
        ])


# Retry only rate-limit and server errors
def should_retry(error):
    return (
        isinstance(error, APIStatusError)
        and (
            error.status_code == 429
            or 500 <= error.status_code <= 599
        )
    )


@retry(
    retry=retry_if_exception(should_retry),
    wait=wait_random_exponential(multiplier=1, max=30),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
def create_stream(messages):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=500,
        stream=True,
        stream_options={"include_usage": True}
    )


# Conversation history
messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Give clear and concise answers."
    }
]

print("\n========== AI CHATBOT ==========")
print("Type 'exit' to quit.\n")

while True:
    try:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        print("\nAI: ", end="", flush=True)

        stream = create_stream(messages)

        ai_reply = ""
        usage = None
        actual_model = MODEL

        for chunk in stream:
            if chunk.model:
                actual_model = chunk.model

            if chunk.choices:
                content = chunk.choices[0].delta.content

                if content:
                    print(content, end="", flush=True)
                    ai_reply += content

            if chunk.usage is not None:
                usage = chunk.usage

        print("\n")

        if ai_reply:
            messages.append({
                "role": "assistant",
                "content": ai_reply
            })

        if usage:
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            estimated_cost = getattr(usage, "cost", None)

            with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now(timezone.utc).isoformat(),
                    actual_model,
                    input_tokens,
                    output_tokens,
                    estimated_cost if estimated_cost is not None else ""
                ])

            print(f"Input tokens: {input_tokens}")
            print(f"Output tokens: {output_tokens}")
            print(
                "Estimated cost (USD):",
                estimated_cost if estimated_cost is not None else "Not provided"
            )
            print("Usage saved to cost_log.csv")
        else:
            print("Token usage was not returned by the provider.")

        print("--------------------------------")

    except KeyboardInterrupt:
        print("\n\nChatbot stopped.")
        break

    except Exception as error:
        if messages and messages[-1]["role"] == "user":
            messages.pop()

        print("\nError:", error)
        print("The request could not be completed.")

