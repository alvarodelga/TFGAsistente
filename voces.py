from elevenlabs import generate, stream

audio_stream = generate(
  text="This is a... streaming voice!!",
  stream=True
)

stream(audio_stream)



