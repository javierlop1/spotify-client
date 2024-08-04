import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

today = datetime.date.today()
first_day_of_last_month = today.replace(day=1) - datetime.timedelta(days=1)
start_date = first_day_of_last_month.replace(day=1).isoformat()

playlists = sp.search(q='genre:rock', type='playlist', limit=10)

tracks = []
for playlist in playlists['playlists']['items']:
    playlist_tracks = sp.playlist_tracks(playlist['id'])
    for item in playlist_tracks['items']:
        track = item['track']
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity']
        })

top_tracks = sorted(tracks, key=lambda x: x['popularity'], reverse=True)

for track in top_tracks:
    print(f"{track['name']} - {track['artist']} (Popularity: {track['popularity']})")
