from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from pathlib import Path
import os
import time
from collections import deque

load_dotenv()

class RateLimiter:
    def __init__(self, max_calls: int = 1, period: float = 2.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def acquire(self):
        now = time.time()
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()

        if len(self.calls) >= self.max_calls:
            wait = self.period - (now - self.calls[0])
            time.sleep(wait)
            now = time.time()
            while self.calls and now - self.calls[0] > self.period:
                self.calls.popleft()

        self.calls.append(time.time())

RATE_LIMITER = RateLimiter(max_calls=2, period=1.0)

class GeminiTranscriber:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key.strip())
        self.model_name = "gemini-2.5-flash"

    def transcribe(self, audio_path):
        audio_path = Path(audio_path)

        max_retries = 4
        backoff = 1.0

        for attempt in range(1, max_retries + 1):
            RATE_LIMITER.acquire()
            try:
                uploaded_file = self.client.files.upload(file=audio_path)
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[
                        uploaded_file,
                        "Transcribe this audio exactly as spoken. Keep punctuation natural."
                    ]
                )
                return response.text
            except (genai_errors.ServerError, genai_errors.ClientError) as e:
                status_code = getattr(e, "status_code", None)
                if status_code in (429, 503) and attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise

model = GeminiTranscriber()