from pathlib import Path
from PreProcessing.extractAudio import extract_audio
from PreProcessing.extractText import extract_text

BASE_DIR = Path(__file__).resolve().parent.parent


def preprocess(videos):
    for video in videos:
        audio_files = extract_audio(video)
        extract_text(audio_files)


if __name__ == "__main__":
    assets_dir = BASE_DIR / "Assets"
    preprocess([assets_dir])
    