import os
import logging
import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

from blogger_api_client import BlogPost, get_credentials
from chatgpt_api import get_openai_response
from logging_config import setup_logging

setup_logging()  # Ensure the logger is set up
logger = logging.getLogger(__name__)

class Track:
    def __init__(self, name, artist, popularity, release_date, description):
        """
        Initializes a Track object with the given attributes.

        Args:
            name (str): The name of the track.
            artist (str): The name of the artist.
            popularity (int): The popularity score of the track.
            release_date (str): The release date of the track.
            description (str): A description or extra information about the track.
        """
        self.name = name
        self.artist = artist
        self.popularity = popularity
        self.release_date = release_date
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.artist} (Popularity: {self.popularity}, Release Date: {self.release_date}, Description: {self.description})"


def authenticate_spotify():
    """
    Authenticates the user with Spotify using OAuth 2.0.
    Requires 'playlist-modify-public' and 'playlist-modify-private' scopes.

    Returns:
        spotipy.Spotify: Authenticated Spotify client.
    """
    try:
        sp_oauth = SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope="playlist-modify-public playlist-modify-private"
        )
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        logger.info("Successfully authenticated with Spotify!")
        return sp
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        raise


class SpotifyRockTracks:
    """
    Class for managing Spotify authentication and retrieving songs.
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
            self.sp = authenticate_spotify()
            logger.info("Initialization successful.")
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            self.sp = None

    def get_rock_playlists(self, limit=10):
        """
        Retrieves the most popular rock playlists from the Spotify API.

        Args:
            limit (int): Maximum number of playlists to retrieve. Default is 10.

        Returns:
            list: A list of popular rock playlists.
        """
        try:
            playlists = self.sp.search(q='genre:rock,year:2024,week:21', type='playlist', limit=limit)
            logger.info(f"Retrieved {len(playlists['playlists']['items'])} rock playlists.")
            return playlists['playlists']['items']
        except spotipy.exceptions.SpotifyException as e:
            logger.error(f"Error retrieving Spotify playlists: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving playlists: {e}")
            raise

    def get_rock_tracks_week_year(self, limit=5, week_of_the_year=12, year=2024):
        """
        Retrieves rock tracks released in the specified week and year.

        Args:
            limit (int): Maximum number of tracks to retrieve. Default is 5.
            week_of_the_year (int): The week number of the year.
            year (int): The year.

        Returns:
            list: A list of track objects (songs) from the specified week and year in the rock genre.
        """
        try:
            query = f'genre=hard rock,year={year},week={week_of_the_year}'
            logger.info(f"Spotify query: {query}")
            results = self.sp.search(q=query, type='track', limit=limit)

            tracks = []
            for i, item in enumerate(results['tracks']['items'], start=1):
                song = Track(
                    name=item['name'],
                    artist=item['artists'][0]['name'],
                    popularity=item['popularity'],
                    release_date=item['album']['release_date'],
                    description=get_track_description(item, str(i))
                )
                tracks.append(song)

            logger.info(f"Retrieved {len(tracks)} rock tracks from week {week_of_the_year} of {year}.")
            return tracks
        except spotipy.exceptions.SpotifyException as e:
            logger.error(f"Error retrieving tracks: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving tracks: {e}")
            return []

    def get_playlist_tracks(self, playlist_id):
        """
        Retrieves the tracks from a specific Spotify playlist.

        Args:
            playlist_id (str): The ID of the playlist on Spotify.

        Returns:
            list: A list of Track objects from the playlist.
        """
        try:
            playlist_tracks = self.sp.playlist_tracks(playlist_id)
            songs = [
                Track(
                    name=item['track']['name'],
                    artist=item['track']['artists'][0]['name'],
                    popularity=item['track']['popularity']
                )
                for item in playlist_tracks['items']
            ]
            logger.info(f"Retrieved {len(songs)} tracks from playlist {playlist_id}.")
            return songs
        except spotipy.exceptions.SpotifyException as e:
            logger.error(f"Error retrieving playlist tracks: {e}")
            return []
        except KeyError as e:
            logger.error(f"Key error while processing tracks: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving playlist tracks: {e}")
            return []

    def get_top_rock_tracks(self, limit_playlists=5):
        """
        Retrieves the most popular rock tracks from multiple playlists.

        Args:
            limit_playlists (int): Maximum number of playlists to process. Default is 5.

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
            logger.info(f"Retrieved a total of {len(top_songs)} songs.")
            return top_songs
        except Exception as e:
            logger.error(f"Error retrieving top tracks: {e}")
            return []

    def display_top_tracks_text(self, top_songs):
        """
        Returns the most popular rock tracks formatted as a text string.

        Args:
            top_songs (list): List of top songs.

        Returns:
            str: A text string containing the list of songs.
        """
        if not self.sp:
            logger.error("Cannot display tracks due to authentication issues.")
            return "<p>Error: Cannot display tracks due to authentication issues.</p>"

        try:
            if top_songs:
                text_output = ""
                for song in top_songs[:5]:
                    text_output += song.description
                logger.info(f"Generated text for {len(top_songs)} songs: {text_output}")
                return text_output
            else:
                logger.warning("No songs found to display.")
                return "No songs found to display."
        except Exception as e:
            logger.error(f"Error displaying tracks: {e}")
            return f"Error displaying tracks: {e}"

    def display_top_tracks_html(self, top_songs):
        """
        Returns the most popular rock tracks formatted as an HTML string.

        Args:
            top_songs (list): List of top songs.

        Returns:
            str: An HTML string containing the list of songs.
        """
        if not self.sp:
            logger.error("Cannot display tracks due to authentication issues.")
            return "<p>Error: Cannot display tracks due to authentication issues.</p>"

        try:
            if top_songs:
                html_output = ""
                for i, song in enumerate(top_songs[:5], start=1):
                    html_output += f"<p><b>{i} - {song.name}</b> - <b>{song.artist}</b> - Release date: {song.release_date}<br>\n"
                    html_output += f"{song.description}<br><br></p>"
                logger.info(f"Generated HTML for {len(top_songs)} songs.")
                return html_output
            else:
                logger.warning("No songs found to display.")
                return "<p>No songs found to display.</p>"
        except Exception as e:
            logger.error(f"Error displaying tracks: {e}")
            return f"<p>Error displaying tracks: {e}</p>"

    def create_playlist(self, playlist_name, songs, playlist_description=""):
        """
        Creates a new playlist on Spotify and adds songs to it.

        Args:
            playlist_name (str): The name of the new playlist.
            songs (list): A list of Track objects representing the songs to add to the playlist.
            playlist_description (str): Optional description for the playlist.

        Returns:
            str: The link to the created playlist.
        """
        try:
            logger.info(f"playlist to create: {playlist_name}")

            # Verify if the user is authenticated
            if not self.sp:
                logger.error("Error: the user is not authenticated to create a playlist.")
                return None

            # Get the         
            user_profile = self.sp.me()
            logger.info(f"Authenticated user: {user_profile['display_name']}")

            # Create a new playlist
            playlist = self.sp.user_playlist_create(user=user_profile['id'], name=playlist_name, public=True, description=playlist_description)
            playlist_id = playlist['id']

            # Get the URIs of the songs (URI is required to add songs to a playlist)
            track_uris = []
            for song in songs:
                # Search for the song on Spotify to get its URI
                query = f"{song.name} {song.artist}"
                result = self.sp.search(q=query, type='track', limit=1)

                if result['tracks']['items']:
                    track_uri = result['tracks']['items'][0]['uri']
                    track_uris.append(track_uri)
                else:
                    logger.warning(f"Song not found: {song.name} by {song.artist} on Spotify.")

            # Add the songs to the created playlist
            if track_uris:
                self.sp.playlist_add_items(playlist_id, track_uris)
                logger.info(f"Playlist '{playlist_name}' created with {len(track_uris)} songs.")
            else:
                logger.warning(f"No songs were added to the playlist '{playlist_name}' because no valid URIs were found.")

            # Return the link to the created playlist
            playlist_url = playlist['external_urls']['spotify']
            return playlist_url

        except Exception as e:
            logger.error(f"Error creating the playlist: {e}")
            return None #in case of error, we don't want to return anything, to not block the program.
        

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
    logging.info(f"Week number: {result}")

    
    return result

def get_track_description(track, position):
    return get_openai_response(f"Can you write the introduction for this song: {track['name']} from {track['artists'][0]['name']}, as if you were the author of a rock music blog which present a list with the top rock songs,  the first thing that has to be mentioned is that this is the song number {position} in the list, You should omit the introduction from the response, I just want the text for the blog, and the response should be no more than 35 words.")

# Main execution
if __name__ == "__main__":
    # Instantiate the SpotifyRockTracks class
    spotify_rock_tracks = SpotifyRockTracks()

    # Get the current week of the year
    week_of_the_year = str(get_today_week_of_year())

    # Retrieve top rock songs for the current week and year
    top_songs = spotify_rock_tracks.get_rock_tracks_week_year(limit=5, week_of_the_year=week_of_the_year, year=2024)
    
    # Reverse the order of the list (optional, based on your logic)
    top_songs.reverse()

    # Define your Blogger blog ID
    blog_id = '7624840374831160388'  # Replace with your actual blog ID

    # Generate a title for the blog post
    title = f'Top Rock Songs for Week {week_of_the_year}'

    # Generate an introduction for the blog post using OpenAI
    introduction_text = get_openai_response(
        "Can you write the introduction for a list with the top rock songs for this week as if you were the author of a rock music blog? "
        "You should omit the introduction from the response. I just want the text for the blog, and the response should be no more than 35 words."
    )

    # Format the blog content in HTML
    content = f'<p>{introduction_text}</p>'
    content += spotify_rock_tracks.display_top_tracks_html(top_songs)

    # Generate a text for video description
    text_for_video = introduction_text + spotify_rock_tracks.display_top_tracks_text(top_songs)

    # Create a Spotify playlist for the top rock songs of the current week
    playlist_name = f"Top Rock Anthems for Week {week_of_the_year}"
    playlist_description = f"Top rock anthems for week {week_of_the_year}"
    playlist_url = spotify_rock_tracks.create_playlist(playlist_name, top_songs, playlist_description)

    # Add playlist link to the blog content
    content_footer = f'<p><span style="font-size: x-small;">This list has been created with AI using Spotify data and some magic. You can find the <a href="{playlist_url}">playlist here</a>.</span></p>'
    content += content_footer

    # Get credentials for Blogger API
    creds = get_credentials()

    # Create an instance of BlogPost with the blog ID, title, content, and credentials
    blog_post = BlogPost(blog_id, title, content, creds)
    
    # Publish the blog post
    blog_post.create_post()

    # Print a confirmation message
    logging.info(f"Blog post titled '{title}' was successfully published.")
