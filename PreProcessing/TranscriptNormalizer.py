"""
TranscriptNormalizer
====================
Cleans up raw Whisper transcripts (garbled Hinglish, mixed Hindi/English,
Devanagari, hallucinated text) into semantically accurate clean English
using Gemini Flash.

- Overwrites the transcript file in-place (no new file created)
- One API call per video transcript (entire file in one prompt)
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv()

PROMPT = (
    "Below is a raw speech-to-text transcript of a Hinglish YouTube video "
    "(a mix of Hindi and English, possibly in Devanagari script, Roman script, "
    "or garbled/hallucinated text from the ASR model). "
    "Convert it into proper Hinglish — Roman-script Hindi mixed with English — "
    "exactly as a YouTuber would naturally speak and write it. "
    "Preserve the EXACT meaning, specific vocabulary, and cultural nuance. "
    "Keep English terms like 'next gen colleges', 'alumni network', 'batch pass out', "
    "fees amounts, brand names, and numbers exactly as they are in the original meaning. "
    "Preserve the line-by-line structure — same number of lines. "
    "Do NOT translate to full English. Do NOT use Devanagari. "
    "Do NOT add markdown formatting or commentary.\n\n"
    "Example style: 'saare next gen colleges pichle 2-3 saal mein establish hue, "
    "matlab abhi tak ek bhi batch pass out nahi hua hai'\n\n"
    "Raw Transcript:\n{text}\n\n"
    "Hinglish Transcript:\n"
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key.strip())
MODEL_NAME = "gemini-2.5-flash"


def _normalize_text(text: str) -> str:
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
                print(f"[TranscriptNormalizer] Rate limited. Retrying in {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise


def normalize_transcripts(transcript_files: list) -> None:
    """
    Normalize each transcript file in-place.
    One Gemini API call per file (= one full video transcript per call).

    Parameters
    ----------
    transcript_files : list[Path]
        List of transcript .txt paths returned by extract_text().
    """
    for transcript_file in transcript_files:
        transcript_file = Path(transcript_file)
        raw_text = transcript_file.read_text(encoding="utf-8").strip()

        if not raw_text:
            print(f"[TranscriptNormalizer] Skipping empty: {transcript_file.name}")
            continue

        print(f"[TranscriptNormalizer] Normalizing '{transcript_file.name}' (1 API call) ...")
        clean_text = _normalize_text(raw_text)

        transcript_file.write_text(clean_text, encoding="utf-8")
        print(f"[TranscriptNormalizer] Saved in-place → {transcript_file.name}")
        print(f"  Snippet: {clean_text[:120]}...\n")
