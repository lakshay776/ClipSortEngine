from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PreProcessing.extractAudio import extract_audio
from PreProcessing.extractText import extract_text
from VectorEngine.vector_generation import vector_engine
from PreProcessing.ScriptPipeline import ScriptPipeline
from PreProcessing.TranscriptNormalizer import normalize_transcripts
from SearchEngine.Search import search
from Paths import SCRIPTS


def preprocess(videos):
    all_transcriptions= []
    audio_files=[]
    
    for video in videos:
        audio_files = extract_audio(video)
        all_transcriptions.extend(extract_text(audio_files))
    normalize_transcripts(all_transcriptions)  # clean garbled Hinglish → English before embedding
    vector_engine(all_transcriptions)
    for script in SCRIPTS.glob("*.txt"):
        if script.name.startswith("Normalized_"):
            continue   # skip normalized outputs — they are not source scripts
        ScriptPipeline(script)
    search()
    


   


if __name__ == "__main__":
    assets_dir = BASE_DIR / "Assets"
    preprocess([assets_dir])
    