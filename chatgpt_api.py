import os
import openai
import logging
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Retrieve API key from environment variable (loaded from .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


if not openai.api_key:
    raise ValueError("API key not found. Make sure OPENAI_API_KEY is set in the .env file.")


def get_chatgpt_response(user_message, model="gpt-4o-mini"):
    """
    Sends a user message to the OpenAI API and retrieves the model's response.

    Args:
        user_message (str): The input message from the user.
        model (str): The name of the OpenAI model to use. Defaults to 'gpt-4o-mini'.

    Returns:
        str: The model's response or an error message if an exception occurs.
    """
    try:
        # Log the model and message being sent
        logging.info(f"Requesting response from model '{model}' with message: {user_message}")
        
        # API call to OpenAI
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=60,  # Limit the number of tokens in the response
            temperature=0.7,  # Adjust the creativity level (0.0 - 1.0)
        )

        # Return the generated response from the model
        return response['choices'][0]['message']['content']
    
    except openai.error.InvalidRequestError as e:
        logging.error(f"Invalid request: {e}")
        return f"Error: Invalid request - {e}"
    
    except openai.error.AuthenticationError as e:
        logging.error(f"Authentication error: {e}")
        return f"Error: Authentication failed - check your API key."

    except openai.error.RateLimitError as e:
        logging.warning(f"Rate limit exceeded: {e}")
        return "Error: Rate limit exceeded, please try again later."
    
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return f"Error: An unexpected error occurred - {e}"


def get_response(user_message, model="gpt-4o-mini"):
    """
    Sends a user message to the OpenAI API and retrieves the model's response.


    Args:
        user_message (str): The input message from the user.
        model (str): The name of the OpenAI model to use. Defaults to 'gpt-4o-mini'.


    Returns:
        str: The model's response or an error message if an exception occurs.
    """
    try:
        # Log the model and message being sent
        logging.info(f"Requesting response from model '{model}' with message: {user_message}")
       
        # API call to OpenAI
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=60,  # Limit the number of tokens in the response
            temperature=0.7,  # Adjust the creativity level (0.0 - 1.0)
        )


        # Return the generated response from the model
        return response['choices'][0]['message']['content']
   
    except openai.error.InvalidRequestError as e:
        logging.error(f"Invalid request: {e}")
        return f"Error: Invalid request - {e}"
   
    except openai.error.AuthenticationError as e:
        logging.error(f"Authentication error: {e}")
        return f"Error: Authentication failed - check your API key."


    except openai.error.RateLimitError as e:
        logging.warning(f"Rate limit exceeded: {e}")
        return "Error: Rate limit exceeded, please try again later."
   
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return f"Error: An unexpected error occurred - {e}"


def main(user_message):
    """
    Main function that takes a user message as a parameter and displays the model's response.


    Args:
        user_message (str): The input message from the user.
    """
    try:
        # Fetch response from the model
        response = get_response(user_message)
       
        # Display the response
        print(f"Model response: {response}")
   
    except Exception as e:
        logging.exception("An error occurred in the main program.")


# Example usage
if __name__ == "__main__":
    main("Can you write the introduction for a list with the top rock songs for this week as if you were the author of a rock music blog, You should omit the introduction from the response, I just want the text for the blog, and the response should be no more than 35 words.")
    #main("Can you write the introduction for this song: Ama by Extremoduro, as if you were the author of a rock music blog which present a list with the top rock songs,  the first thing that has to be mentioned is that this is the song number 2 in the list, You should omit the introduction from the response, I just want the text for the blog, and the response should be no more than 35 words.")