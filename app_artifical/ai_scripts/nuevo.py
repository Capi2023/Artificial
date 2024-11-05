import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el CSV
df = pd.read_csv('static\otros\dataset.csv')

# Normalizar las columnas numéricas relevantes
numeric_features = ['popularity', 'tempo', 'valence', 'danceability', 'energy', 'loudness',
                    'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'duration_ms']
scaler = MinMaxScaler()
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# One-hot encoding para el género
encoder = OneHotEncoder(sparse_output=False)
genres_encoded = encoder.fit_transform(df[['track_genre']])

# Crear DataFrame para géneros codificados
genres_encoded_df = pd.DataFrame(genres_encoded, columns=encoder.get_feature_names_out())

# Definir los pesos de cada característica
weights = {
    'genre': 3.0,
    'popularity': 2.0,
    'tempo': 2.5,
    'valence': 2.0,
    'danceability': 2.2,
    'energy': 2.0,
    'loudness': 1.0,
    'speechiness': 1.0,
    'acousticness': 1.0,
    'instrumentalness': 1.0,
    'liveness': 1.0,
    'duration_ms': 2.1
}

# Crear un nuevo DataFrame con las características ponderadas
weighted_features_df = pd.DataFrame()
for feature, weight in weights.items():
    if feature == 'genre':
        weighted_genres = genres_encoded_df * weight
        weighted_features_df = pd.concat([weighted_features_df, weighted_genres], axis=1)
    else:
        weighted_features_df[f'{feature}_weighted'] = df[feature] * weight

# Unir todas las características ponderadas con el DataFrame original
df = pd.concat([df, weighted_features_df], axis=1)

# Seleccionar las características ponderadas para el modelo
weighted_features = list(weighted_features_df.columns)
X = df[weighted_features].values

# Función para recomendar canciones similares a una canción específica considerando explicit
def recomendar_canciones(nombre_cancion, df, X, num_recomendaciones=5):
    # Encontrar la fila de la canción seleccionada por el nombre
    idx_cancion = df.index[df['track_name'].str.lower() == nombre_cancion.lower()].tolist()[0]

    # Obtener las características de la canción seleccionada
    cancion_seleccionada = X[idx_cancion].reshape(1, -1)
    explicit_seleccionada = df.loc[idx_cancion, 'explicit']

    # Calcular similitudes de coseno con todas las demás canciones
    similitudes = cosine_similarity(cancion_seleccionada, X)

    # Ordenar canciones por similitud
    indices_similares = np.argsort(similitudes[0])[::-1]

    # Excluir la propia canción seleccionada de las recomendaciones y filtrar por explicit
    indices_similares = [i for i in indices_similares if i != idx_cancion and df.loc[i, 'explicit'] == explicit_seleccionada]

    # Obtener las canciones recomendadas
    canciones_recomendadas = df.iloc[indices_similares[:num_recomendaciones]]

    return canciones_recomendadas

# Ejemplo: Seleccionar una canción por su nombre y obtener recomendaciones
nombre_cancion = 'Avec Toi'  # Cambiar por el nombre de la canción
recomendaciones = recomendar_canciones(nombre_cancion, df, X)

# Mostrar las recomendaciones con sus nombres, géneros, y otras características
print(f"Recomendaciones para la canción '{nombre_cancion}':")
for i, row in recomendaciones.iterrows():
    print(f"Nombre: {row['track_name']}, Artista: {row['artists']}, Álbum: {row['album_name']}, Género: {row['track_genre']}, Popularidad: {row['popularity']}, Tempo: {row['tempo']}, Valencia: {row['valence']}, Danceability: {row['danceability']}, Energy: {row['energy']}")

