from pathlib import Path
from models.whisper_engine import model


def extract_text(audio):
    if isinstance(audio, (list, tuple)):
        for audio_path in audio:
            _transcribe(audio_path)
        return
    _transcribe(audio)


def _transcribe(audio_path):
    audio_path = Path(audio_path)
    segments, info = model.transcribe(str(audio_path))
    for segment in segments:
        print(segment.start, segment.end, segment.text)

