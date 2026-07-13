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
from Renaming.Sort import Sort
from Renaming.Renaming import Rename


RESULTS = BASE_DIR / "Results"
_STALE_FILES = [
    RESULTS / "line_mapping.json",
    RESULTS / "sorted_file_sequence.json",
]

def preprocess(videos):
    # Clear stale result files from any previous run
    for f in _STALE_FILES:
        if f.exists():
            f.unlink()
            print(f"Cleared stale file: {f.name}")

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
    Sort()
    Rename()
    print("*************************************************************")
    print("*************************************************************")
    print("*************************************************************")
    print("*************************************************************")
    print("-----------------------Renaming Done-------------------------")

   


if __name__ == "__main__":
    assets_dir = BASE_DIR / "Assets"
    preprocess([assets_dir])
    