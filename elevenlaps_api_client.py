import requests
import os

def text_to_speech(text: str, api_key: str, voice_id: str, output_filename: str = "output.mp3"):
    """
    Converts text to speech using ElevenLabs API and saves the result as an mp3 file.

    :param text: The text to convert to speech.
    :param api_key: Your ElevenLabs API key for authentication.
    :param voice_id: The ID of the voice to use from ElevenLabs.
    :param output_filename: The filename for the output mp3 file.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    # Send POST request to the API
    response = requests.post(url, headers=headers, json=data)

    # Check if request was successful
    if response.status_code == 200:
        # Save the response content (audio) as an mp3 file
        with open(output_filename, "wb") as file:
            file.write(response.content)
        print(f"MP3 file saved as {output_filename}")
    else:
        print(f"Error: Unable to generate speech. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage
api_key = "sk_89dfe47a7ba8fd20e3175d95d2e67a4a56cbcae22cbac637"  # Replace with your ElevenLabs API key
voice_id = "CwhRBWXzGAHq8TQ4Fs17"  # Replace with the desired voice ID from ElevenLabs
text = "Hello, this is a sample text to speech conversion using ElevenLabs."
output_filename = "speech_output.mp3"

text_to_speech(text, api_key, voice_id, output_filename)
