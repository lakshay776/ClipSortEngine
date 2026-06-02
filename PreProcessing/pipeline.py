from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PreProcessing.extractAudio import extract_audio
from PreProcessing.extractText import extract_text
from VectorEngine.vector_generation import vector_engine
from PreProcessing.ScriptPipeline import ScriptPipeline
from Paths import SCRIPTS


def preprocess(videos):
    all_transcriptions= []
    audio_files=[]
    
    for video in videos:
        audio_files = extract_audio(video)
        all_transcriptions.extend(extract_text(audio_files))
    vector_engine(all_transcriptions)
    for script in SCRIPTS.glob("*.txt"):
        ScriptPipeline(script)
    


   


if __name__ == "__main__":
    assets_dir = BASE_DIR / "Assets"
    preprocess([assets_dir])
    