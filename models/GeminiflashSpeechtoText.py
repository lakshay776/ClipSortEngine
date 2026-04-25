# AIzaSyAAUP1lq_MzNxlfiG7iR4hKH-_v03MhhFc

from google import genai
from pathlib import Path

class GeminiTranscriber:
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyAAUP1lq_MzNxlfiG7iR4hKH-_v03MhhFc")
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