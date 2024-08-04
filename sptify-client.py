import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Autenticación
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Obtener la fecha de hace un mes
today = datetime.date.today()
first_day_of_last_month = today.replace(day=1) - datetime.timedelta(days=1)
start_date = first_day_of_last_month.replace(day=1).isoformat()

# Obtener las playlists de rock más populares
playlists = sp.search(q='genre:rock', type='playlist', limit=10)

# Obtener las canciones de las playlists
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

# Ordenar las canciones por popularidad
top_tracks = sorted(tracks, key=lambda x: x['popularity'], reverse=True)

# Imprimir las canciones de rock más escuchadas del mes pasado
for track in top_tracks:
    print(f"{track['name']} - {track['artist']} (Popularity: {track['popularity']})")
