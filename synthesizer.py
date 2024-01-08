import torch
from TTS.api import TTS


def text_to_speech_coqui_single_speaker(text, output_file, language_model):
	# Get device
	device = "cuda" if torch.cuda.is_available() else "cpu"

	# List available TTS models
	print(f'Model List: {TTS().list_models().list_tts_models()}')

	# Init TTS
	tts = TTS("tts_models/es/css10/vits", progress_bar=True).to(device)

	# Run TTS
	tts.tts_to_file(text=text, file_path=output_file)

def text_to_speech_coqui_multiple_speaker(text, output_file, language_model):
	# Get device
	device = "cuda" if torch.cuda.is_available() else "cpu"

	# List available 🐸TTS models
	print(f'Model List: {TTS().list_models().list_tts_models()}')

	# Init TTS
	tts = TTS("tts_models/es/css10/vits", progress_bar=True).to(device)

	# Run TTS
	tts.tts_to_file(text=text, speaker_wav='./workdirectory/speaker_audio.wav', file_path=output_file)