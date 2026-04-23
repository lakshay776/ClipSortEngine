from faster_whisper import WhisperModel

model = WhisperModel("large-v3", compute_type="int8")
segments, info= model.transcribe("Assets/videoplayback2.aac")

for segment in segments:
    print(segment.start, segment.end,segment.text)
