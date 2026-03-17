import whisper

model = whisper.load_model("base")


def generate_transcript(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]