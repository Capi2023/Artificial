# ai_scripts/simple_recommender.py
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()

# Usar las variables de entorno
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Diccionario simple de canciones por género (IA básica)
song_database = {
    'rock': ['Bohemian Rhapsody - Queen', 'Stairway to Heaven - Led Zeppelin', 'Hotel California - Eagles'],
    'pop': ['Bad Guy - Billie Eilish', 'Blinding Lights - The Weeknd', 'Shape of You - Ed Sheeran'],
    'hiphop': ['Sicko Mode - Travis Scott', 'God\'s Plan - Drake', 'Rockstar - Post Malone'],
    'canadian pop': ['Blinding Lights - The Weeknd']  # Si el género devuelto es "canadian pop"
}

# Función para configurar la autenticación con Spotify
def spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    )

# Función para obtener el género de una canción usando Spotify
def get_genre_from_spotify(track_id, token):
    sp = Spotify(auth=token)
    track_info = sp.track(track_id)
    
    # Spotify no proporciona directamente géneros de canciones individuales, pero puedes obtener el género del artista
    artist_id = track_info['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    
    if artist_info and artist_info['genres']:
        # Devolver el primer género del artista
        return artist_info['genres'][0]
    return None

# Recomendador basado en géneros con integración a Spotify
def recommend_songs(track_id, token):
    genre = get_genre_from_spotify(track_id, token)  # Obtiene el género de Spotify

    print(f"Género obtenido de Spotify: {genre}")  # Imprime el género en la consola para depurar

    if genre in song_database:
        # Si el género está en la IA básica, devuelve recomendaciones predefinidas
        return song_database[genre]
    else:
        # Si no se encuentra el género en la IA, no hay recomendaciones
        return ['No recommendations available for this genre']