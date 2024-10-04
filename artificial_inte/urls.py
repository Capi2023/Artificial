from django.contrib import admin
from django.urls import path
from app_artifical import views
from app_artifical.views import *

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('spotify_login/', spotify_login, name='spotify_login'),  # Ruta para iniciar sesión en Spotify
    path('callback/', spotify_callback, name='spotify_callback'),  # Ruta para manejar la redirección de Spotify
    path('spotify_recommend/', recommend_view, name='spotify_recommend'),  # Ruta para ver las recomendaciones
    path('spotify_recommend_with_ia/', recommend_view_with_ia, name='spotify_recommend_with_ia'),  # Usa esta para probar la IA
]
