import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import logging
from dotenv import load_dotenv

from BloggerClient import BlogPost, get_credentials

import datetime

# Logging configuration
logging.basicConfig(
    level=logging.INFO,  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Message format
    handlers=[
        logging.FileHandler("spotify_rock_tracks.log"),  # Save logs to a file
        logging.StreamHandler()  # Display logs in the console
    ]
)

class Cancion:
    """
    Class that represents a song.

    Attributes:
        name (str): The name of the song.
        artist (str): The name of the artist.
        popularity (int): The popularity level of the song (0-100).
    """

    def __init__(self, name, artist, popularity):
        """
        Initializes an instance of the Cancion class.

        Args:
            name (str): The name of the song.
            artist (str): The name of the artist.
            popularity (int): The popularity level of the song.
        """
        self.name = name
        self.artist = artist
        self.popularity = popularity

    def __str__(self):
        """
        Returns a string representation of the song.

        Returns:
            str: A string describing the song.
        """
        return f"{self.name} - {self.artist} (Popularity: {self.popularity})"


class SpotifyRockTracks:
    """
    Class for managing Spotify authentication and retrieving songs.

    Attributes:
        client_id (str): Spotify API client ID.
        client_secret (str): Spotify API client secret.
        sp (spotipy.Spotify): Authenticated Spotipy instance to make API requests.
    """

    def __init__(self):
        """
        Initializes an instance of SpotifyRockTracks. Loads credentials from a .env file and authenticates with the Spotify API.
        """
        try:
            load_dotenv()  # Load environment variables from the .env file
            self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
            self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
            if not self.client_id or not self.client_secret:
                raise ValueError("Spotify credentials are not properly configured.")
            self.sp = self.authenticate()
            logging.info("Initialization successful.")
        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            self.sp = None

    def authenticate(self):
        """
        Authenticates with the Spotify API using the provided credentials.

        Returns:
            spotipy.Spotify: Authenticated Spotipy instance if successful, otherwise None.
        """
        try:
            client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            logging.info("Successfully authenticated with Spotify.")
            return sp
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Authentication error with Spotify: {e}")
            return None

    def get_rock_playlists(self, limit=10):
        """
        Retrieves the most popular rock playlists from the Spotify API.

        Args:
            limit (int): Maximum number of playlists to retrieve. Default is 10.

        Returns:
            list: A list of popular rock playlists.
        """
        try:
            playlists = self.sp.search(q='genre:rock,year:2024,week:21', type='track', limit=limit)
            logging.info(f"Retrieved {len(playlists['playlists']['items'])} rock playlists.")
            return playlists['playlists']['items']
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error retrieving Spotify playlists: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error retrieving playlists: {e}")
            return []
        
    def get_rock_tracks_week_year(self, limit=10, week_of_the_year=12, year=2024):
        """
        Retrieves rock tracks released in the 12th week of 2024.

        Args:
            limit (int): Maximum number of tracks to retrieve. Default is 10.

        Returns:
            list: A list of track objects (songs) from the 12th week of 2024 in the rock genre.
        """
        try:
            # Search for rock songs released in the 12th week of 2024
            query = 'genre=rock,year=2024,week='+str(week_of_the_year)
            results = self.sp.search(q=query, type='track', limit=limit)
            
            tracks = []
            for item in results['tracks']['items']:
                track = item
                song = Cancion(
                    name=track['name'],
                    artist=track['artists'][0]['name'],
                    popularity=track['popularity']
                )
                tracks.append(song)
            
            logging.info(f"Retrieved {len(tracks)} rock tracks from the 12th week of 2024.")
            return tracks
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error retrieving tracks: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error retrieving tracks: {e}")
            return []    

    def get_playlist_tracks(self, playlist_id):
        """
        Retrieves the tracks from a specific Spotify playlist.

        Args:
            playlist_id (str): The ID of the playlist on Spotify.

        Returns:
            list: A list of Cancion objects from the playlist.
        """
        try:
            playlist_tracks = self.sp.playlist_tracks(playlist_id)
            songs = []
            for item in playlist_tracks['items']:
                track = item['track']
                song = Cancion(
                    name=track['name'],
                    artist=track['artists'][0]['name'],
                    popularity=track['popularity']
                )
                songs.append(song)
            logging.info(f"Retrieved {len(songs)} tracks from playlist {playlist_id}.")
            return songs
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error retrieving playlist tracks: {e}")
            return []
        except KeyError as e:
            logging.error(f"Key error while processing tracks: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error retrieving playlist tracks: {e}")
            return []

    def get_top_rock_tracks(self, limit_playlists=10):
        """
        Retrieves the most popular rock tracks from multiple playlists.

        Args:
            limit_playlists (int): Maximum number of playlists to process. Default is 10.

        Returns:
            list: A list of the most popular tracks, sorted by popularity.
        """
        try:
            playlists = self.get_rock_playlists(limit=limit_playlists)
            all_songs = []
            for playlist in playlists:
                songs = self.get_playlist_tracks(playlist['id'])
                all_songs.extend(songs)
            top_songs = sorted(all_songs, key=lambda x: x.popularity, reverse=True)
            logging.info(f"Retrieved a total of {len(top_songs)} songs.")
            return top_songs
        except Exception as e:
            logging.error(f"Error retrieving top tracks: {e}")
            return []

    def display_top_tracks(self, limit_playlists=10, week_of_year=12):
        """
        Returns the most popular rock tracks formatted as an HTML string.

        Args:
            limit_playlists (int): Maximum number of playlists to process to retrieve tracks. Default is 10.

        Returns:
            str: An HTML string containing the list of songs.
        """
        if not self.sp:
            logging.error("Cannot display tracks due to authentication issues.")
            return "<p>Error: Cannot display tracks due to authentication issues.</p>"
        
        try:
            top_songs = self.get_rock_tracks_week_year(limit_playlists, week_of_year)
            if top_songs:
                html_output = "<ul>\n"
                for song in top_songs:
                    html_output += f"<li>{song.name} - {song.artist} (Popularity: {song.popularity})</li>\n"
                html_output += "</ul>"
                logging.info(f"Generated HTML for {len(top_songs)} songs.")
                return html_output
            else:
                logging.warning("No songs found to display.")
                return "<p>No songs found to display.</p>"
        except Exception as e:
            logging.error(f"Error displaying tracks: {e}")
            return f"<p>Error displaying tracks: {e}</p>"

def get_today_week_of_year():
    """
    Returns the current date in European format (DD/MM/YYYY) and the current week of the year.
    
    Returns:
        str: A string containing today's date in DD/MM/YYYY format and the week number.
    """
    today = datetime.date.today()
    # European date format: DD/MM/YYYY
    european_format = today.strftime('%d/%m/%Y')
    # Get the current week number of the year
    week_number = today.isocalendar()[1]
    
    # Create the final string
    result = week_number
    
    return result

# Main execution
if __name__ == "__main__":
    spotify_rock_tracks = SpotifyRockTracks()
    

    blog_id = '7624840374831160388'  # Replace with your actual blog ID
    title = 'Top rock songs for week '+str(get_today_week_of_year())
    content = '<p>'+spotify_rock_tracks.display_top_tracks(10,get_today_week_of_year())+'</p>'

    # Obtain credentials
    creds = get_credentials()

    # Create an instance of BlogPost with blog ID, title, content, and credentials
    blog_post = BlogPost(blog_id, title, content, creds)
    
    # Publish the post
    blog_post.create_post()
