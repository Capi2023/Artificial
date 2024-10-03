import os
from django.shortcuts import render, redirect
from .ai_scripts.simple_recommender import recommend_songs
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .ai_scripts.simple_recommender import recommend_songs, get_genre_from_spotify
import time
from dotenv import load_dotenv
load_dotenv()

# Usar las variables de entorno
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

def index(request):
    return render(request, 'index.html')


def recommend_view(request):
    recommendations = []
    if request.method == 'POST':
        genre = request.POST.get('genre')
        recommendations = recommend_songs(genre)

    return render(request, 'recommend_form.html', {'recommendations': recommendations})


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

# Vista para manejar el callback de redirección desde Spotify
def spotify_callback(request):
    sp_oauth = spotify_auth()
    
    # Obtiene el código de autorización de la URL (después del callback de Spotify)
    code = request.GET.get('code')
    
    # Intercambia el código de autorización por un token de acceso
    token_info = sp_oauth.get_access_token(code)
    
    # Almacena tanto el token de acceso como el refresh token en la sesión
    request.session['token_info'] = token_info

    return redirect('spotify_recommend_with_ia')

# Vista para obtener recomendaciones de Spotify
def recommend_from_spotify(track_id, token):
    sp = Spotify(auth=token)  # Usa el token para autenticar la API de Spotify
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)  # Obtiene recomendaciones
    return recommendations['tracks']

# Vista para mostrar el formulario y las recomendaciones
def recommend_view(request):
    token_info = request.session.get('token_info', None)  # Obtiene el token de la sesión
    recommendations = []

    # Si no hay token, redirige al usuario para iniciar sesión en Spotify
    if not token_info:
        return redirect('spotify_login')

    # Si el usuario envía un track ID, obtenemos recomendaciones
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        recommendations = recommend_from_spotify(track_id, token_info['access_token'])

    return render(request, 'spotify_recommend_form.html', {'recommendations': recommendations})


def is_token_expired(token_info):
    now = int(time.time())  # Ahora se utilizará el módulo 'time' correctamente
    return token_info['expires_at'] - now < 60  # Considera expirado si faltan menos de 60 segundos

def refresh_token_if_needed(request):
    token_info = request.session.get('token_info', None)  # Obtiene el token de la sesión

    # Si no hay token en la sesión, redirige al inicio de sesión de Spotify
    if token_info is None:
        return None  # Devuelve None para manejarlo en la vista principal

    sp_oauth = spotify_auth()

    if is_token_expired(token_info):
        # Refrescar el token
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        request.session['token_info'] = token_info  # Actualiza la sesión con el nuevo token
    
    return token_info

def recommend_view_with_ia(request):
    token_info = refresh_token_if_needed(request)  # Refresca el token si ha expirado

    # Si no hay token (es None), redirige al usuario para iniciar sesión en Spotify
    if token_info is None:
        return redirect('spotify_login')

    recommendations = []
    genre = None

    # Si el usuario envía un Track ID, obtenemos el género y usamos la IA para recomendar
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        genre = get_genre_from_spotify(track_id, token_info['access_token'])  # Obtiene el género de Spotify
        recommendations = recommend_songs(track_id, token_info['access_token'])  # Obtiene las recomendaciones

    # Pasamos tanto las recomendaciones como el género a la plantilla
    return render(request, 'ia.html', {'recommendations': recommendations, 'genre': genre})

