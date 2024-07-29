import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

# Tus credenciales de Spotify
CLIENT_ID = 'e04bd24832424ea2a2e7312f78dac2a3'
CLIENT_SECRET = 'f3337d65f36b4d5ba6b7f97fdf911c99'

# Autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Función para obtener las canciones más escuchadas en una categoría específica (e.g., "rock")
def get_top_tracks_for_genre(sp, genre, country='US', limit=20):
    results = sp.search(q=f'genre:{genre}', type='track', limit=limit, market=country)
    tracks = results['tracks']['items']
    return tracks

# Obtener las canciones de rock más escuchadas
top_rock_tracks = get_top_tracks_for_genre(sp, 'rock')

# Imprimir los resultados
for idx, track in enumerate(top_rock_tracks):
    print(f"{idx+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

# Opcional: guardar los resultados en un archivo
with open('top_rock_tracks.txt', 'w') as f:
    for idx, track in enumerate(top_rock_tracks):
        f.write(f"{idx+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n")