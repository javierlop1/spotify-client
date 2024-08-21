import pytest
from unittest import mock
from spotify_rock_tracks import SpotifyRockTracks, Cancion

# Test de la autenticación exitosa
def test_autenticacion_exitosa(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    spotify_rock_tracks = SpotifyRockTracks()
    
    assert spotify_rock_tracks.sp is not None
    mock_spotify.assert_called_once()

# Test de autenticación fallida
def test_autenticacion_fallida(mocker):
    mocker.patch('spotify_rock_tracks.Spotify', side_effect=mock.Mock(side_effect=Exception('Error')))
    spotify_rock_tracks = SpotifyRockTracks()
    
    assert spotify_rock_tracks.sp is None

# Test para obtener playlists de rock exitosamente
def test_obtener_playlists_rock_exito(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    mock_spotify.return_value.search.return_value = {'playlists': {'items': [{'id': '1', 'name': 'Rock Playlist 1'}]}}
    
    spotify_rock_tracks = SpotifyRockTracks()
    playlists = spotify_rock_tracks.obtener_playlists_rock()
    
    assert len(playlists) == 1
    assert playlists[0]['name'] == 'Rock Playlist 1'

# Test para obtener playlists de rock con error
def test_obtener_playlists_rock_error(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    mock_spotify.return_value.search.side_effect = Exception('Error inesperado')
    
    spotify_rock_tracks = SpotifyRockTracks()
    playlists = spotify_rock_tracks.obtener_playlists_rock()
    
    assert playlists == []

# Test para obtener canciones de una playlist con éxito
def test_obtener_canciones_de_playlist_exito(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    mock_spotify.return_value.playlist_tracks.return_value = {
        'items': [{
            'track': {
                'name': 'Song 1',
                'artists': [{'name': 'Artist 1'}],
                'popularity': 80
            }
        }]
    }
    
    spotify_rock_tracks = SpotifyRockTracks()
    canciones = spotify_rock_tracks.obtener_canciones_de_playlist('playlist_id')
    
    assert len(canciones) == 1
    assert canciones[0].nombre == 'Song 1'
    assert canciones[0].artista == 'Artist 1'
    assert canciones[0].popularidad == 80

# Test para manejar un error al obtener canciones de una playlist
def test_obtener_canciones_de_playlist_error(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    mock_spotify.return_value.playlist_tracks.side_effect = Exception('Error inesperado')
    
    spotify_rock_tracks = SpotifyRockTracks()
    canciones = spotify_rock_tracks.obtener_canciones_de_playlist('playlist_id')
    
    assert canciones == []

# Test para obtener las canciones de rock más populares
def test_obtener_top_canciones_rock(mocker):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    
    # Mock para la respuesta de la búsqueda de playlists
    mock_spotify.return_value.search.return_value = {
        'playlists': {
            'items': [
                {'id': 'playlist_id_1'},
                {'id': 'playlist_id_2'}
            ]
        }
    }
    
    # Mock para la respuesta de la obtención de canciones de cada playlist
    mock_spotify.return_value.playlist_tracks.side_effect = [
        {
            'items': [
                {'track': {'name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'popularity': 80}},
                {'track': {'name': 'Song 2', 'artists': [{'name': 'Artist 2'}], 'popularity': 70}},
            ]
        },
        {
            'items': [
                {'track': {'name': 'Song 3', 'artists': [{'name': 'Artist 3'}], 'popularity': 90}},
                {'track': {'name': 'Song 4', 'artists': [{'name': 'Artist 4'}], 'popularity': 60}},
            ]
        }
    ]
    
    spotify_rock_tracks = SpotifyRockTracks()
    top_canciones = spotify_rock_tracks.obtener_top_canciones_rock(limite_playlists=2)
    
    # Verificar que las canciones estén ordenadas por popularidad
    assert len(top_canciones) == 4
    assert top_canciones[0].nombre == 'Song 3'
    assert top_canciones[1].nombre == 'Song 1'
    assert top_canciones[2].nombre == 'Song 2'
    assert top_canciones[3].nombre == 'Song 4'

# Test para mostrar las canciones de rock más populares
def test_mostrar_top_canciones(mocker, capsys):
    mock_spotify = mocker.patch('spotify_rock_tracks.Spotify')
    
    # Mock para la respuesta de la búsqueda de playlists
    mock_spotify.return_value.search.return_value = {
        'playlists': {
            'items': [
                {'id': 'playlist_id_1'}
            ]
        }
    }
    
    # Mock para la respuesta de la obtención de canciones de cada playlist
    mock_spotify.return_value.playlist_tracks.return_value = {
        'items': [
            {'track': {'name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'popularity': 80}},
            {'track': {'name': 'Song 2', 'artists': [{'name': 'Artist 2'}], 'popularity': 70}},
        ]
    }
    
    spotify_rock_tracks = SpotifyRockTracks()
    spotify_rock_tracks.mostrar_top_canciones(limite_playlists=1)
    
    # Capturar la salida estándar (print statements)
    captured = capsys.readouterr()
    
    # Verificar que las canciones se imprimieron correctamente
    assert "Song 1 - Artist 1 (Popularity: 80)" in captured.out
    assert "Song 2 - Artist 2 (Popularity: 70)" in captured.out
