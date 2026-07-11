"""
ScriptNormalizer
================
Translates a Hinglish script file to clean English using Gemini Flash.

Output: VideoScript/Normalized_<original_filename>.txt
Skips re-normalization if the file already exists (cache).
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv()

PROMPT = (
    "Translate the following Hinglish script (Roman-script Hindi mixed with English) "
    "into clean English. Keep proper nouns, numbers, and brand names as-is.\n"
    "CRITICAL: Preserve the exact line-by-line structure. Return exactly the same "
    "number of lines. If a line is blank, leave it blank. Do not add markdown formatting.\n\n"
    "Hinglish Script:\n{text}\n\n"
    "English Script:\n"
)

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key.strip())
MODEL_NAME = "gemini-2.5-flash"


def _translate_script(text: str) -> str:
    max_retries = 3
    backoff = 4.0

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=PROMPT.format(text=text),
            )
            return response.text.strip()
        except (genai_errors.ServerError, genai_errors.ClientError) as e:
            status_code = getattr(e, "status_code", None)
            if status_code in (429, 503) and attempt < max_retries:
                print(f"[ScriptNormalizer] Rate limited. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise


def normalize_script(script_file: Path, force: bool = False) -> Path:
    script_file  = Path(script_file)
    output_file  = script_file.parent / f"Normalized_{script_file.name}"

    if output_file.exists() and not force:
        print(f"[ScriptNormalizer] Using cached {output_file.name}")
        return output_file

    print(f"[ScriptNormalizer] Normalizing '{script_file.name}' with Gemini Flash (1 API call) ...")
    
    script_text = script_file.read_text(encoding="utf-8")
    
    # Translate entire script in one go to avoid 5 RPM limits
    translated_text = _translate_script(script_text)
    
    output_file.write_text(translated_text, encoding="utf-8")
    print(f"[ScriptNormalizer] Saved → {output_file}")
    
    # Just to show what happened
    print(f"[ScriptNormalizer] Output snippet:\n{translated_text[:150]}...\n")
    
    return output_file
