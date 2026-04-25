from pathlib import Path
from models.GeminiflashSpeechtoText import model
from PreProcessing.Paths import TEMP_TEXT

TEMP_TEXT.mkdir(exist_ok=True,parents=True)

def extract_text(audio):
    if isinstance(audio, (list, tuple)):
        for audio_path in audio:
            _transcribe(audio_path)
        return
    _transcribe(audio)


def _transcribe(audio_path):
    audio_path = Path(audio_path)
    transcript = model.transcribe(str(audio_path))
    transcript_file = TEMP_TEXT / f"{audio_path.stem}.txt"

    if isinstance(transcript, (list, tuple)):
        lines = []
        for segment in transcript:
            text = getattr(segment, "text", str(segment)).strip()
            lines.append(text)
            print(text)
        full_text = "\n".join(lines)
    else:
        full_text = str(transcript)
        print(full_text)

    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"{audio_path} added to {transcript_file}")

