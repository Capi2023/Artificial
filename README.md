# Artificial

![](https://github.com/Capi2023/Artificial/blob/main/static/imagens/Captura%20de%20pantalla%202024-10-03%20125221.png)

![](https://github.com/Capi2023/Artificial/blob/main/static/imagens/Captura%20de%20pantalla%202024-10-03%20125233.png)

![](https://github.com/Capi2023/Artificial/blob/main/static/imagens/Captura%20de%20pantalla%202024-10-03%20125249.png)


Para instalar un proyecto de Django desde GitHub en tu PC, sigue estos pasos:

### 1. Clonar el repositorio desde GitHub
Primero, necesitas clonar el repositorio en tu computadora. Abre una terminal o consola y ejecuta el siguiente comando, reemplazando `URL_DEL_REPOSITORIO` por la URL del repositorio de GitHub:

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Navegar al directorio del proyecto
Una vez que hayas clonado el repositorio, navega al directorio del proyecto:

```bash
cd nombre_del_proyecto
```

### 3. Crear un entorno virtual
Es recomendable utilizar un entorno virtual para instalar las dependencias del proyecto. Si no tienes instalado `virtualenv`, puedes instalarlo usando pip:

```bash
pip install virtualenv
```

Luego, crea un entorno virtual:

```bash
virtualenv venv
```

Activa el entorno virtual:

- En Windows:
  ```bash
  venv\Scripts\activate
  ```
- En macOS o Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Instalar las dependencias del proyecto
Normalmente, el proyecto tendrá un archivo `requirements.txt` que contiene todas las dependencias necesarias. Puedes instalar esas dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

### 5. Configurar la base de datos
Dependiendo del proyecto, es posible que debas configurar la base de datos. En la mayoría de los casos, esto implica aplicar las migraciones del proyecto. Ejecuta los siguientes comandos para aplicar las migraciones de la base de datos:

```bash
python manage.py migrate
```

### 6. Crear un archivo `.env` (opcional)
Si el proyecto utiliza un archivo `.env` para la configuración de variables de entorno (como claves secretas o credenciales), asegúrate de crear este archivo en la raíz del proyecto siguiendo las instrucciones en el archivo README del repositorio o en el código fuente. Copia el contenido de un archivo `.env.example` si existe.

### 7. Crear un superusuario (opcional)
Si necesitas acceso a la interfaz de administración de Django, crea un superusuario:

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor de desarrollo
Finalmente, puedes ejecutar el servidor de desarrollo para verificar que todo esté funcionando correctamente:

```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000/` en tu navegador para ver el proyecto en funcionamiento.
