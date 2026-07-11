from pathlib import Path
# from models.GeminiflashSpeechtoText import model
from models.whisper_engine import model
from PreProcessing.Paths import TEMP_TEXT

TEMP_TEXT.mkdir(exist_ok=True,parents=True)

def extract_text(audio):
    all_transcriptions = []
    if isinstance(audio, (list, tuple)):
        for audio_path in audio:
            _transcribe(audio_path, all_transcriptions)
    elif audio is not None:
        _transcribe(audio, all_transcriptions)
    return all_transcriptions


def _transcribe(audio_path, all_transcriptions):

    audio_path = Path(audio_path)
    # faster_whisper returns (segments_generator, TranscriptionInfo)
    segments, info = model.transcribe(str(audio_path))
    transcript_file = TEMP_TEXT / f"{audio_path.stem}.txt"

    print(f"Detected language: {info.language} ({info.language_probability:.2%})")

    lines = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            lines.append(text)
            print(text)

    full_text = "\n".join(lines)

    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"{audio_path} added to {transcript_file}")
    all_transcriptions.append(transcript_file)




