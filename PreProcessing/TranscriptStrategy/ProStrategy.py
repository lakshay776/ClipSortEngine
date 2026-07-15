
from pathlib import Path
from .extractAudio import extract_audio
from models.GroqSTT import client
from PreProcessing.Paths import TEMP_TEXT

TEMP_TEXT.mkdir(parents=True, exist_ok=True)


def ProStrategy(videos):
    audio_files = []
    transcript_files = []
    for video in videos:
        audio_files = extract_audio(video)
        for audio in audio_files:
            with open(audio, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    file=(audio.name, f.read()),
                    model="whisper-large-v3",
                    temperature=0,
                    response_format="verbose_json",
                )

            # Save transcript text to .txt file (same format as FreeStrategy)
            transcript_file = TEMP_TEXT / f"{Path(audio).stem}.txt"
            text = "\n".join(seg.text.strip() for seg in transcription.segments if seg.text.strip())
            transcript_file.write_text(text, encoding="utf-8")

            print(f"{audio} --> {transcript_file}")
            transcript_files.append(transcript_file)

    return transcript_files
