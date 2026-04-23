import ffmpeg
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_AUDIO = BASE_DIR / "Temp" / "Audio"
TEMP_AUDIO.mkdir(parents=True, exist_ok=True)
SUPPORTED_EXTENSIONS = {".aac", ".mp4", ".mov", ".mkv", ".wav", ".flac"}


def extract_audio(video):
    video_path = Path(video)
    if video_path.is_dir():
        audio_files = []
        for input_file in sorted(video_path.iterdir()):
            if input_file.is_file() and input_file.suffix.lower() in SUPPORTED_EXTENSIONS:
                audio_files.append(_extract_audio_file(input_file))
        return audio_files
    return [_extract_audio_file(video_path)]


def _extract_audio_file(video_file: Path):
    audio = TEMP_AUDIO / f"{video_file.stem}.aac"
    (
        ffmpeg
        .input(str(video_file))
        .output(str(audio), acodec="copy", vn=None)
        .run(overwrite_output=True)
    )
    return audio