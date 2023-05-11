import speech_recognition as sr
import whisper
from scipy.io import wavfile
import openai
import pyttsx3
from pytube import YouTube
import os
from elevenlabs import voices, generate
from elevenlabs import set_api_key
from elevenlabs import generate, play

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"  # or any other model you'd like to use
r = sr.Recognizer()
model = whisper.load_model("base")
set_api_key("6c0848206e09337d3eaafb954460afd6")
voices = voices()



def voicerec():
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        with open("audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        fs, data = wavfile.read("audio.wav")
        text_dict = model.transcribe("audio.wav", fp16=False, language='es')
        text_str = text_dict["text"].lower()  # Convertir el valor de la clave "text" a una cadena en minúsculas
        print(text_str)
        return text_str


def transvideo():
    model = whisper.load_model("base")
    result = model.transcribe("VideoAudio.mp3", fp16=False)
    print(result["text"])
    nombre_archivo = "transcripcion.txt"
    with open(nombre_archivo, "w") as archivo:
        archivo.write(result["text"])

def comanddetection(text_str):

    conversacion = "ordenador"
    comando = "comando"

    try:
        if conversacion in text_str:
            # Extraer el texto que sigue a "ordenador activate"
            command = text_str.split(conversacion)[1]
            command = "ordenador " + command
            print("Peticion:", command)
            return command
        elif comando in text_str:
            # Extraer el texto que sigue a "comando"
            command = "comando"
            print("Comando:", command)
            return command
    except sr.UnknownValueError:
        print("Lo siento, no he entendido lo que has dicho")
    except sr.RequestError as e:
        print(f"No puedo conectarme con el servicio de reconocimiento de voz; {e}")


def gptturbo(command):

    messages = [{"role": "system",
                 "content": "Eres un asistente virtual con un toque hirónico, tu nombre es ordenador y cada vez que me dirija a ti te llamare ordenador, tus respuestas no deben ser demasiado largas "}]

    content = command

    messages.append({"role": "user",
                     "content": content})

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages)

    response_content = response.choices[0].message.content

    print(response_content)
    return response_content


def speaker(consulta):
    audio = generate(
        text=consulta,
        voice="alvaro",
        model='eleven_multilingual_v1')

    play(audio)

def speaker2(consulta):
    audio = generate(
        text=consulta,
        voice="alvaro",
        model='eleven_multilingual_v1')

    play(audio)

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


def main():
    while True:
        text_str = voicerec()
        command = comanddetection(text_str)

        if command:
            print("artriba")
            print(command.split(" ")[0])
            print("abajo")
            if command.split(" ")[0] == "ordenador":
                if "comando" in command:
                    print("Comando detectado")
                    if "descargar" or "descargar" or "descargame" or "descarga" in command:
                        print("descaregando video...")
                        consulta = "Descargando y transcribiendo el video"
                        speaker(consulta)
                        videoyoutube()
                        transvideo()

                else:
                    consulta = gptturbo(command)
                    speaker(consulta)
            elif command.split(" ")[0] == "comando":
                print("preguntar que coamando quiere activar")





if __name__ == "__main__":
    main()

