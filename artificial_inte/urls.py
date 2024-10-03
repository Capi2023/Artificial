"""
URL configuration for artificial_inte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
