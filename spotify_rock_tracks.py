import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import logging
from dotenv import load_dotenv




# Configuración del logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de los mensajes
    handlers=[
        logging.FileHandler("spotify_rock_tracks.log"),  # Guardar logs en un archivo
        logging.StreamHandler()  # Mostrar logs en la consola
    ]
)

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
        try:
            load_dotenv()  # Cargar las variables de entorno desde el archivo .env
            self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
            self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
            if not self.client_id or not self.client_secret:
                raise ValueError("Las credenciales de Spotify no están configuradas correctamente.")
            self.sp = self.autenticar()
            logging.info("Inicialización exitosa.")
        except Exception as e:
            logging.error(f"Error durante la inicialización: {e}")
            self.sp = None

    def autenticar(self):
        try:
            # Autenticación con Spotify API
            client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            logging.info("Autenticación con Spotify exitosa.")
            return sp
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error de autenticación con Spotify: {e}")
            return None

    def obtener_playlists_rock(self, limite=10):
        try:
            # Obtener las playlists de rock más populares
            playlists = self.sp.search(q='genre:rock', type='playlist', limit=limite)
            logging.info(f"Se obtuvieron {len(playlists['playlists']['items'])} playlists de rock.")
            return playlists['playlists']['items']
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error al obtener playlists de Spotify: {e}")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al obtener playlists: {e}")
            return []

    def obtener_canciones_de_playlist(self, playlist_id):
        try:
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
            logging.info(f"Se obtuvieron {len(canciones)} canciones de la playlist {playlist_id}.")
            return canciones
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error al obtener canciones de la playlist: {e}")
            return []
        except KeyError as e:
            logging.error(f"Error de clave al procesar las canciones: {e}")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al obtener canciones de la playlist: {e}")
            return []

    def obtener_top_canciones_rock(self, limite_playlists=10):
        try:
            # Obtener las canciones de rock más populares de varias playlists
            playlists = self.obtener_playlists_rock(limite=limite_playlists)
            todas_las_canciones = []
            for playlist in playlists:
                canciones = self.obtener_canciones_de_playlist(playlist['id'])
                todas_las_canciones.extend(canciones)
            # Ordenar las canciones por popularidad
            top_canciones = sorted(todas_las_canciones, key=lambda x: x.popularidad, reverse=True)
            logging.info(f"Se obtuvieron un total de {len(top_canciones)} canciones.")
            return top_canciones
        except Exception as e:
            logging.error(f"Error al obtener las canciones más populares: {e}")
            return []

    def mostrar_top_canciones(self, limite_playlists=10):
        if not self.sp:
            logging.error("No se puede mostrar las canciones debido a problemas de autenticación.")
            return
        try:
            # Imprimir las canciones de rock más escuchadas
            top_canciones = self.obtener_top_canciones_rock(limite_playlists=limite_playlists)
            if top_canciones:
                for cancion in top_canciones:
                    print(cancion)
                    logging.info(f"Canción: {cancion}")
            else:
                logging.warning("No se encontraron canciones para mostrar.")
        except Exception as e:
            logging.error(f"Error al mostrar las canciones: {e}")

# Ejecución principal
if __name__ == "__main__":
    spotify_rock_tracks = SpotifyRockTracks()
    spotify_rock_tracks.mostrar_top_canciones()
