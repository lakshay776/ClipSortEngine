from dotenv import load_dotenv
from google import genai
from pathlib import Path
import os

load_dotenv()

class GeminiTranscriber:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
       
        self.client = genai.Client(api_key=api_key.strip())
        self.model_name = "gemini-2.5-flash"

    def transcribe(self, audio_path):
        audio_path = Path(audio_path)

        uploaded_file = self.client.files.upload(
            file=audio_path
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                uploaded_file,
                "Transcribe this audio exactly as spoken. Keep punctuation natural."
            ]
        )

        return response.text

model = GeminiTranscriber()