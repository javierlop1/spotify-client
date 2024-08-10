# Spotify Rock Tracks Analyzer

This project retrieves the most popular rock tracks from Spotify playlists using the Spotify API. It is implemented in Python with an object-oriented approach, handling exceptions and logging detailed information.

## Features

- **Fetch Rock Playlists:** Retrieves popular rock playlists from Spotify.
- **Extract Songs:** Extracts songs from these playlists and ranks them by popularity.
- **Exception Handling:** Robust handling of potential errors during API calls and data processing.
- **Logging:** Detailed logging of all operations and errors, both in the console and in a log file.

## Prerequisites

Before running the project, ensure you have the following:

- **Python 3.7+**
- **Spotify Developer Account:** Obtain your Spotify API credentials.
- **Pip Packages:** Required Python packages can be installed via `pip`.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/spotify-rock-tracks-analyzer.git
   cd spotify-rock-tracks-analyzer
## Setup

2. **Install Required Packages:**

   Install the necessary Python packages using pip:

   ```bash
   pip install spotipy python-dotenv


3. **Setup Environment Variables:**

   Create a `.env` file in the project root directory and add your Spotify API credentials:

   ```bash
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret   

4. **Run the Script:**

   Execute the script to fetch and display the top rock tracks:

   ```bash
   python spotify-client.py   