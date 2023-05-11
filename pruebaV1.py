import speech_recognition as sr
import whisper
from scipy.io import wavfile
import openai
import pyttsx3
from pytube import YouTube
import os

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"  # or any other model you'd like to use
r = sr.Recognizer()
model = whisper.load_model("base")



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
            command = text_str.split(comando, 1)[1].strip()
            print("Comando:", command)
            return command
    except sr.UnknownValueError:
        print("Lo siento, no he entendido lo que has dicho")
    except sr.RequestError as e:
        print(f"No puedo conectarme con el servicio de reconocimiento de voz; {e}")


def gptturbo(command, messages):

    messages = [{"role": "system",
                 "content": "Eres un asistente virtual muy útil"}]

    content = command

    messages.append({"role": "user",
                     "content": content})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages)

    response_content = response.choices[0].message.content

    messages.append({"role": "assistant",
                     "content": response_content})

    print(response_content)
    print(messages)
    return response_content


def speaker(consulta):
    engine = pyttsx3.init()
    engine.setProperty("rate",150)
    engine.say(consulta)
    print("deberiua hablar")
    print(consulta)
    engine.runAndWait()


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
    global messages
    messages = []
    while True:
        text_str = voicerec()
        command = comanddetection(text_str)
        if command:
            consulta = gptturbo(command,messages)
            speaker(consulta)




if __name__ == "__main__":
    main()











