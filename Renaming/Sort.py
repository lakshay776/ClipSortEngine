

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent  # ClipSort/
RESULTS = ROOT / "Results"

seen={}

def Sort():
    with open(RESULTS / "line_mapping.json") as filemap:
        FileMapping = json.load(filemap)

        for entry in FileMapping:
            top_file= entry["matches"][0]["transcript_file"]
            if top_file not in seen:
                seen[top_file] = len(seen)+1

    with open(RESULTS / "sorted_file_sequence.json", "w") as out:
        json.dump(seen, out, indent=4)
    print("Saved sorted_file_sequence.json")


if __name__ == "__main__":
    Sort()
    for filename, index in seen.items():
        print(f"Renaming {filename} to {index}")
                
    