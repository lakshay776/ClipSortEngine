import os 
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent  # ClipSort/
ASSETS_DIR = ROOT / "Assets"
RESULTS = ROOT / "Results"

def Rename():
    with open(RESULTS / "sorted_file_sequence.json", "r") as f:
        SortedMap = json.load(f)

    for transcript_path, index in SortedMap.items():
        # Get the stem from the transcript file e.g. "1" from "1.txt"
        stem = os.path.splitext(os.path.basename(transcript_path))[0]

        # Find the matching video file in Assets/ with the same stem
        match = None
        for asset_file in os.listdir(ASSETS_DIR):
            asset_stem = os.path.splitext(asset_file)[0]
            if asset_stem == stem:
                match = asset_file
                break

        if match is None:
            print(f"No video found in Assets for transcript: {transcript_path}")
            continue

        ext = os.path.splitext(match)[1]                      # e.g. ".MOV"
        old_path = Path(ASSETS_DIR) / match
        new_path = Path(ASSETS_DIR) / f"{index}{ext}"         # e.g. "1.MOV"

        if old_path == new_path:
            print(f"Already named correctly: {match}")
            continue

        old_path.replace(new_path)  # overwrites destination on Windows safely
        print(f"Renamed: {match} -> {index}{ext}")

if __name__ == "__main__":
    Rename()