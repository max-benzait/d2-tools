# File Duplication GUI

Este proyecto proporciona una interfaz gráfica de usuario (GUI) para duplicar y versionar archivos entre directorios en macOS y Ubuntu. También incluye una función de actualización automática desde un repositorio de Git.

## Requisitos

- Python 3.x
- `tkinter`
- `python-dotenv`
- `pyinstaller`
- Git

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu-usuario/d2-tools.git
    cd d2-tools
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En macOS o Linux
    venv\Scripts\activate  # En Windows
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido, ajustando las rutas según sea necesario:
    ```env
    MAC_SRC=/Users/maxramirez/Desktop/diablo2save/Diablo II Resurrected
    MAC_DST=/System/Volumes/Data/Users/maxramirez/Library/Application Support/CrossOver/Bottles/Diablo II Resurrected/drive_c/users/crossover/Saved Games/Diablo II Resurrected
    UBUNTU_SRC=/home/max/Desktop/diablo2save/Diablo II Resurrected
    UBUNTU_DST=/home/max/.local/share/Steam/steamapps/compatdata/2710268825/pfx/drive_c/users/steamuser/Saved Games/Diablo II Resurrected
    ```

## Uso

### Ejecutar la Aplicación

Para ejecutar la aplicación, simplemente corre:

```sh
python main.py
