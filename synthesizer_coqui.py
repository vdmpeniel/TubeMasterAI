import torch
from TTS.api import TTS


def text_to_speech_coqui_single_speaker(text, output_file, language_model):
	device = "cuda" if torch.cuda.is_available() else "cpu"
	print(f'Model List: {TTS().list_models().list_tts_models()}')
	tts = TTS("tts_models/es/mai/tacotron2-DDC", progress_bar=True).to(device)
	tts.tts_to_file(text=text, file_path=output_file)



def text_to_speech_coqui_multiple_speaker(text, output_file, language_model='en', speaker_name='Claribel Dervla'):
	device = "cuda" if torch.cuda.is_available() else "cpu"
	print(f'Model List: {TTS().list_models().list_tts_models()}')
	tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=True).to(device)

	print(f'Is this a multi lingual model?: {tts.is_multi_lingual}')
	if hasattr(tts, 'languages'):
		print(f'Language List: {tts.languages}')

	print(f'Is this a multi speaker model?: {tts.is_multi_speaker}')
	speaker_list = tts.synthesizer.tts_model.speaker_manager.speakers.keys()
	print(f'Speaker list: {speaker_list}')
	if not speaker_name in speaker_list:
		raise Exception('Speaker name is not available')

	tts.tts_to_file(text=text, speaker=speaker_name, language=language_model, file_path=output_file, split_sentences=True)


def text_to_speech_coqui_cloning(text, speaker_wav, output_file, language_model):
	device = "cuda" if torch.cuda.is_available() else "cpu"
	print(f'Model List: {TTS().list_models().list_tts_models()}')
	tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=True).to(device)
	tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language_model, file_path=output_file, split_sentences=True)