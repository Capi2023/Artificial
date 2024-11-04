import os
from django.shortcuts import render, redirect
from .ai_scripts.simple_recommender import recommend_songs, get_track_info_from_spotify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import pandas as pd
from .ai_scripts.nuevo import recomendar_canciones, X, df

load_dotenv()
df = pd.read_csv('static\otros\dataset.csv')

# Usar las variables de entorno
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

def index(request):
    return render(request, 'index.html')


# Función para configurar la autenticación con Spotify
def spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    )

# Vista para redirigir al usuario a la página de autenticación de Spotify
def spotify_login(request):
    sp_oauth = spotify_auth()
    auth_url = sp_oauth.get_authorize_url()  # Obtiene la URL de autorización
    return redirect(auth_url)

# Vista para obtener recomendaciones de Spotify
def recommend_view_spotify(request):
    token_info = request.session.get('token_info', None)  # Obtiene el token de la sesión
    recommendations = []
    if not token_info:
        return redirect('spotify_login')
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        recommendations = recommend_from_spotify(track_id, token_info['access_token'])
    return render(request, 'spotify_recommend_form.html', {'recommendations': recommendations})

# Vista para manejar el callback de redirección desde Spotify
def spotify_callback(request):
    sp_oauth = spotify_auth()
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('spotify_recommend')

def recommend_from_spotify(track_id, token):
    sp = Spotify(auth=token)
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
    return recommendations['tracks']

# Vista para la IA con integración de Spotify
def recommend_view_with_ia(request):
    token_info = refresh_token_if_needed(request)
    if token_info is None:
        return redirect('spotify_login')
    recommendations = []
    track_info = None
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        track_info = get_track_info_from_spotify(track_id, token_info['access_token'])
        recommendations = recommend_songs(track_id, token_info['access_token'])
    return render(request, 'ia.html', {'recommendations': recommendations, 'track_info': track_info})

def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60

def refresh_token_if_needed(request):
    token_info = request.session.get('token_info', None)
    if token_info is None:
        return None
    sp_oauth = spotify_auth()
    if is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        request.session['token_info'] = token_info
    return token_info


# Vista para obtener recomendaciones de la IA

def recomendar_view(request):
    recomendaciones = None  # Inicializar recomendaciones como None
    if request.method == 'POST':
        nombre_cancion = request.POST.get('nombre_cancion')
        recomendaciones_df = recomendar_canciones(nombre_cancion, df, X)
        
        # Verificar si el DataFrame está vacío
        if not recomendaciones_df.empty:
            recomendaciones = recomendaciones_df.to_dict(orient='records')  # Convertir a lista de diccionarios

    return render(request, 'recomendar.html', {'recomendaciones': recomendaciones})
