from pathlib import Path
from models.whisper_engine import model
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
    segments, info = model.transcribe(str(audio_path))
    transcript_file=TEMP_TEXT/f"{audio_path.stem}.txt"
    lines=[]
    for segment in segments:
        lines.append(segment.text.strip())
        print(segment.text)
    full_Text="\n".join(lines)
    with open(transcript_file,"w", encoding="utf-8") as f:
        f.write(full_Text)
        print(f"{audio_path} added to {transcript_file}")
            

