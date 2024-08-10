import unittest
from unittest.mock import patch, MagicMock
from spotify_rock_tracks import SpotifyRockTracks, Cancion

class TestSpotifyRockTracks(unittest.TestCase):

    @patch('spotify_rock_tracks.SpotifyClientCredentials')
    @patch('spotify_rock_tracks.spotipy.Spotify')
    def setUp(self, mock_spotify, mock_credentials):
        # Setup with mocked Spotify API
        self.mock_spotify_instance = mock_spotify.return_value
        self.spotify_rock_tracks = SpotifyRockTracks()

    def test_autenticar_success(self):
        # Test successful authentication
        self.assertIsNotNone(self.spotify_rock_tracks.sp)

    def test_autenticar_failure(self):
        # Test authentication failure due to missing credentials
        with patch('spotify_rock_tracks.SpotifyClientCredentials', side_effect=Exception("Auth Error")):
            spotify_rock_tracks = SpotifyRockTracks()
            self.assertIsNone(spotify_rock_tracks.sp)

    def test_obtener_playlists_rock(self):
        # Mocking response from Spotify API
        mock_playlists = {
            'playlists': {
                'items': [{'id': 'playlist_1'}, {'id': 'playlist_2'}]
            }
        }
        self.mock_spotify_instance.search.return_value = mock_playlists

        playlists = self.spotify_rock_tracks.obtener_playlists_rock(limite=2)
        self.assertEqual(len(playlists), 2)

    def test_obtener_playlists_rock_failure(self):
        # Test failure when fetching playlists
        self.mock_spotify_instance.search.side_effect = Exception("API Error")
        playlists = self.spotify_rock_tracks.obtener_playlists_rock()
        self.assertEqual(playlists, [])

    def test_obtener_canciones_de_playlist(self):
        # Mocking response from Spotify API
        mock_tracks = {
            'items': [
                {'track': {'name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'popularity': 80}},
                {'track': {'name': 'Song 2', 'artists': [{'name': 'Artist 2'}], 'popularity': 85}}
            ]
        }
        self.mock_spotify_instance.playlist_tracks.return_value = mock_tracks

        canciones = self.spotify_rock_tracks.obtener_canciones_de_playlist('playlist_id')
        self.assertEqual(len(canciones), 2)
        self.assertEqual(canciones[0].nombre, 'Song 1')
        self.assertEqual(canciones[1].artista, 'Artist 2')

    def test_obtener_canciones_de_playlist_failure(self):
        # Test failure when fetching songs from a playlist
        self.mock_spotify_instance.playlist_tracks.side_effect = Exception("API Error")
        canciones = self.spotify_rock_tracks.obtener_canciones_de_playlist('playlist_id')
        self.assertEqual(canciones, [])

    def test_obtener_top_canciones_rock(self):
        # Mocking multiple playlist song retrieval
        self.spotify_rock_tracks.obtener_playlists_rock = MagicMock(return_value=[{'id': 'playlist_1'}])
        self.spotify_rock_tracks.obtener_canciones_de_playlist = MagicMock(
            return_value=[
                Cancion(nombre='Song 1', artista='Artist 1', popularidad=80),
                Cancion(nombre='Song 2', artista='Artist 2', popularidad=85)
            ]
        )

        top_canciones = self.spotify_rock_tracks.obtener_top_canciones_rock(limite_playlists=1)
        self.assertEqual(len(top_canciones), 2)
        self.assertEqual(top_canciones[0].nombre, 'Song 2')

    def test_mostrar_top_canciones(self):
        # Mock the top songs retrieval and check output
        with patch('builtins.print') as mocked_print:
            self.spotify_rock_tracks.obtener_top_canciones_rock = MagicMock(
                return_value=[
                    Cancion(nombre='Song 1', artista='Artist 1', popularidad=80)
                ]
            )
            self.spotify_rock_tracks.mostrar_top_canciones(limite_playlists=1)
            mocked_print.assert_called_with('Song 1 - Artist 1 (Popularity: 80)')

if __name__ == '__main__':
    unittest.main()
