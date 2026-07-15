from .extractAudio import extract_audio
from .extractText import extract_text


def free_strategy(videos):
    audio_files = []
    transcriptions = []
    for video in videos:
        audio_files = extract_audio(video)
        transcriptions.extend(extract_text(audio_files))
    return transcriptions