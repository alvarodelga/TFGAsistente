from pytube import YouTube
import os



def videoyoutube():
    # Definimos el enlace del video de YouTube que queremos descargar
    video_link = "https://www.youtube.com/watch?v=J0B_eS0JuNQ&ab_channel=LinkinParkSubtitulos"

    # Creamos una instancia de la clase YouTube
    yt = YouTube(video_link, use_oauth=True, allow_oauth_cache=True)

    # Obtenemos la mejor pista de audio disponible
    audio = yt.streams.filter(only_audio=True).first()

    # Definimos el nombre del archivo a descargar
    filename = "VideoAudio.mp3"

    # Comprobamos si el archivo ya existe y lo eliminamos
    if os.path.exists(filename):
        os.remove(filename)

    # Descargamos el audio
    audio.download(output_path="./", filename="temp")

    # Renombramos el archivo de audio descargado con el nombre "VideoAudio.mp3"
    os.rename("temp", filename)