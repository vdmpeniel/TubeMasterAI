import torch
from TTS.api import TTS


def text_to_speech_coqui_single_speaker(text, output_file, language_model):
	# Get device
	device = "cuda" if torch.cuda.is_available() else "cpu"

	# List available 🐸TTS models
	print(f'Model List: {TTS().list_models().list_tts_models()}')

	# Init TTS
	# tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
	tts = TTS("tts_models/en/ljspeech/overflow", progress_bar=True).to(device)

	# Run TTS
	# wav = tts.tts(text=text, language=language_model)
	# Text to speech to a file
	tts.tts_to_file(text=text, file_path=output_file)
