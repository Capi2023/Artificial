from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app_artifical import views
from django.conf.urls.static import static
from app_artifical.views import *

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio
    path('spotify_recommend/', views.recommend_view_spotify, name='spotify_recommend'),  # Recomendaciones de Spotify
    path('spotify_recommend_with_ia/', views.recommend_view_with_ia, name='spotify_recommend_with_ia'),  # IA con Spotify
    path('spotify_login/', views.spotify_login, name='spotify_login'),  # Inicio de sesión de Spotify
    path('callback/', views.spotify_callback, name='spotify_callback'),  # Callback de Spotify
    path('recomendar/', views.recomendar_view, name='recomendar'),  # Recomendaciones de la IA
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
