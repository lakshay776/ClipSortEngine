from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# type 1 = exact script
# type 2 = rough script (to be implemented later)

from VectorEngine.Script_VectorEngine import vector_engine


def ScriptPipeline(script_file, type=1):
    if type == 1:
        # Embed the original Hinglish script directly.
        # Transcript is normalized to Hinglish by TranscriptNormalizer,
        # so both sides share the same vocabulary and register.
        vector_engine(script_file)


if __name__ == "__main__":
    from PreProcessing.Paths import SCRIPTS
    script_files = list(SCRIPTS.glob("*.txt"))
    if not script_files:
        print(f"No .txt script files found in {SCRIPTS}")
    for script in script_files:
        if script.name.startswith("Normalized_"):
            continue
        print(f"Processing: {script.name}")
        ScriptPipeline(script)
