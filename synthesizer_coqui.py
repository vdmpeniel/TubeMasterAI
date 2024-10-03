import torch
from TTS.api import TTS
from absl.logging import exception


def get_model_list():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f'Model List: {TTS().list_models().list_tts_models()}')

def get_model_speaker_list(model='tts_models/multilingual/multi-dataset/xtts_v2'):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model, progress_bar=True).to(device)
    if tts.is_multi_speaker:
        return tts.synthesizer.tts_model.speaker_manager.speakers.keys()
    return []

def get_model_language_list(model='tts_models/multilingual/multi-dataset/xtts_v2'):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model, progress_bar=True).to(device)
    if hasattr(tts, 'languages'):
        return tts.languages
    return []

def text_to_speech_coqui_multiple_speaker(text, output_file, model='tts_models/multilingual/multi-dataset/xtts_v2', language='en', speaker_name='Claribel Dervla'):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model, progress_bar=True).to(device)

    print(f'Is this a multi lingual model?: {tts.is_multi_lingual}')
    print(f'Is this a multi speaker model?: {tts.is_multi_speaker}')
    if not tts.is_multi_speaker:
        raise Exception('Not a multi speaker model')
    tts.tts_to_file(text=text, speaker=speaker_name, language=language, file_path=output_file, split_sentences=True)

def text_to_speech_coqui_single_speaker(text, output_file, model="tts_models/es/mai/tacotron2-DDC"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model, progress_bar=True).to(device)
    print(f'Is this a multi lingual model?: {tts.is_multi_lingual}')
    print(f'Is this a multi speaker model?: {tts.is_multi_speaker}')
    if tts.is_multi_speaker:
        raise Exception('Not a single speaker model')
    print(tts.speakers)
    tts.tts_to_file(text=text, file_path=output_file, split_sentences=True)

def text_to_speech_coqui_cloning(text, speaker_wav, output_file, language='en'):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f'Model List: {TTS().list_models().list_tts_models()}')
    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=True).to(device)
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_file, split_sentences=True)


# VCTK VITS
def vctk_vits_model_reader(text, model='tts_models/en/vctk/vits', speaker='p225', output_path='./'):
    tts = TTS(model)
    tts.tts_to_file(text=text, speaker=speaker, file_path=output_path + '_' + speaker + '.wav')

def get_vctk_vits_speakers_list(model='tts_models/en/vctk/vits'):
    tts = TTS(model)
    return tts.speakers

def create_vctk_vits_model_voice_sampler(model='tts_models/en/vctk/vits', output_path='./'):
    tts = TTS(model)
    print(tts.speakers)
    for speaker in tts.speakers:
        # Choose a male speaker (e.g., Speaker ID 'p225')
        tts.tts_to_file(
            text="This is an English voice sample.",
            speaker=speaker,
            file_path=output_path + '_' + speaker + '.wav'
        )