import os
import openai
import logging
from logging_config import setup_logging
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Setup logger
setup_logging()
logger = logging.getLogger(__name__)

# Retrieve API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("API key not found. Ensure OPENAI_API_KEY is set in the .env file.")

# Constants for OpenAI API call
DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 60

def get_openai_response(user_message, model=DEFAULT_MODEL, temperature=None):
    """
    Send a user message to the OpenAI API and retrieve the model's response.

    Args:
        user_message (str): The input message from the user.
        model (str): The OpenAI model to use.
        temperature (float): Temperature to adjust creativity.

    Returns:
        str: The model's response or error message.
    """
    temperature = temperature if temperature is not None else random.random()

    try:
        # Log the model and message
        logger.info(f"Requesting model '{model}' with message: {user_message}")
        logger.info(f"Using temperature: {temperature}")

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=MAX_TOKENS,
            temperature=temperature,
        )

        return response['choices'][0]['message']['content']
    
    except openai.error.InvalidRequestError as e:
        logger.error(f"Invalid request: {e}")
        return f"Error: Invalid request - {e}"
    
    except openai.error.AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        return f"Error: Authentication failed - check your API key."

    except openai.error.RateLimitError as e:
        logger.warning(f"Rate limit exceeded: {e}")
        return "Error: Rate limit exceeded, please try again later."
    
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        return f"Error: An unexpected error occurred - {e}"

def main(user_message):
    """
    Main function to get and display the model's response.

    Args:
        user_message (str): The input message from the user.
    """
    if not user_message.strip():
        logger.warning("No message provided.")
        return "Error: No message provided."

    try:
        response = get_openai_response(user_message)
        print(f"Model response: {response}")
    except Exception as e:
        logger.exception("An error occurred in the main program.")

# Example usage
if __name__ == "__main__":
    print(main("Hello, ChatGPT!"))
