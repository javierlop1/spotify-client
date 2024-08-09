import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import os
from dotenv import load_dotenv

# Clase que representa una canción
class Cancion:
    def __init__(self, nombre, artista, popularidad):
        self.nombre = nombre
        self.artista = artista
        self.popularidad = popularidad

    def __str__(self):
        return f"{self.nombre} - {self.artista} (Popularity: {self.popularidad})"

# Clase para gestionar la autenticación y la obtención de canciones de Spotify
class SpotifyRockTracks:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.sp = self.autenticar()

    def autenticar(self):
        # Autenticación con Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def obtener_playlists_rock(self, limite=10):
        # Obtener las playlists de rock más populares
        playlists = self.sp.search(q='genre:rock', type='playlist', limit=limite)
        return playlists['playlists']['items']

    def obtener_canciones_de_playlist(self, playlist_id):
        # Obtener las canciones de una playlist específica
        playlist_tracks = self.sp.playlist_tracks(playlist_id)
        canciones = []
        for item in playlist_tracks['items']:
            track = item['track']
            cancion = Cancion(
                nombre=track['name'],
                artista=track['artists'][0]['name'],
                popularidad=track['popularity']
            )
            canciones.append(cancion)
        return canciones

    def obtener_top_canciones_rock(self, limite_playlists=10):
        # Obtener las canciones de rock más populares de varias playlists
        playlists = self.obtener_playlists_rock(limite=limite_playlists)
        todas_las_canciones = []
        for playlist in playlists:
            canciones = self.obtener_canciones_de_playlist(playlist['id'])
            todas_las_canciones.extend(canciones)
        # Ordenar las canciones por popularidad
        top_canciones = sorted(todas_las_canciones, key=lambda x: x.popularidad, reverse=True)
        return top_canciones

    def mostrar_top_canciones(self, limite_playlists=10):
        # Imprimir las canciones de rock más escuchadas
        top_canciones = self.obtener_top_canciones_rock(limite_playlists=limite_playlists)
        for cancion in top_canciones:
            print(cancion)

# Ejecución principal
if __name__ == "__main__":
    spotify_rock_tracks = SpotifyRockTracks()
    spotify_rock_tracks.mostrar_top_canciones()
