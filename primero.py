
import whisper

fp16=False
model = whisper.load_model("base")
result = model.transcribe("audio.mp3", fp16=False, language='es')
print(result["text"])

