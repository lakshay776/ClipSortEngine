from pathlib import Path
import sys

# Ensure ClipSort root is on the path so sibling packages are importable
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# type 1 means exact script 
#type 2 means a rough script will develop the mechanism for this later

from VectorEngine.Script_VectorEngine import vector_engine

def ScriptPipeline(script_file, type=1):
    if type == 1:
        vector_engine(script_file)


if __name__ == "__main__":
    from PreProcessing.Paths import SCRIPTS
    script_files = list(SCRIPTS.glob("*.txt"))
    if not script_files:
        print(f"No .txt script files found in {SCRIPTS}")
    for script in script_files:
        print(f"Processing: {script.name}")
        ScriptPipeline(script)
