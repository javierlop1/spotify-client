import requests
import os
import logging
from logging_config import setup_logging
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException

# Load environment variables from a .env file
load_dotenv()

# Setup logger
setup_logging()
logger = logging.getLogger(__name__)


def text_to_speech(text: str, voice_id: str, output_filename: str = "output.mp3", stability: float = 0.75, similarity_boost: float = 0.75):
    """
    Converts text to speech using the ElevenLabs API with customizable voice settings and saves the result as an MP3 file.

    :param text: The text to convert to speech.
    :param voice_id: The ID of the voice to use from ElevenLabs.
    :param output_filename: The filename for the output mp3 file. Default is "output.mp3".
    :param stability: Controls the stability of the generated speech. Higher values = more stability (default: 0.75).
    :param similarity_boost: Boosts similarity to the target voice. Higher values = closer similarity (default: 0.75).

    :raises ValueError: If text or voice_id is empty or invalid.
    :raises HTTPError: For HTTP issues like a failed API request.
    :raises IOError: If writing the file to disk fails.
    """
    # Get API key from environment variable
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        logger.error("API key not found in environment variables.")
        raise ValueError("Missing API key. Please set ELEVENLABS_API_KEY in the .env file.")

    if not text or not voice_id:
        logger.error("Invalid text or voice_id provided.")
        raise ValueError("Text and Voice ID must be provided and non-empty.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Payload with voice settings
    data = {
        "text": text,
        "voice_settings": {
            "stability": stability,  # Customizable stability
            "similarity_boost": similarity_boost  # Customizable similarity boost
        }
    }

    try:
        # Send POST request to the API
        logger.info(f"Sending request to ElevenLabs API with voice_id={voice_id}, stability={stability}, similarity_boost={similarity_boost}.")
        response = requests.post(url, headers=headers, json=data)

        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        # Write the response content (audio) as an mp3 file
        with open(output_filename, "wb") as file:
            file.write(response.content)

        logger.info(f"MP3 file saved successfully as {output_filename}")

    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise
    except RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise
    except IOError as io_err:
        logger.error(f"File I/O error occurred: {io_err}")
        raise
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise


# Example usage
if __name__ == "__main__":
    try:
        # Customize these parameters as needed
        text = "This is a sample text with customizable voice settings."
        voice_id = "CwhRBWXzGAHq8TQ4Fs17"  # Replace with the actual voice ID
        stability = 0.85  # Higher stability makes the voice more consistent
        similarity_boost = 0.9  # Higher similarity to make it sound closer to the original voice
        output_filename = "customized_voice_output.mp3"

        # Convert text to speech with custom settings
        text_to_speech(text, voice_id, output_filename, stability=stability, similarity_boost=similarity_boost)

    except Exception as e:
        logger.error(f"Failed to complete the text-to-speech operation: {e}")
