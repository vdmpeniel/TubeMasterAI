import pyttsx3
# from TTS.utils.synthesizer import Synthesizer
# from TTS.utils.manage import ModelManager
from gtts import gTTS
import TTS.utils.synthesizer as synthesizer
import TTS as tts
import boto3
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"  # put actual path here


def text_to_speech_pyttsx3(text, output_path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_id = voices[12].id
    print(voice_id)

    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.save_to_file(text, output_path)
    engine.runAndWait()


# Amazon Polly
def text_to_speech_polly(text, output_file):  # Amazon Poly
    polly_client = boto3.client('polly', region_name='us')
    response = polly_client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        VoiceId='Joanna'
    )
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())


# https://gtts.readthedocs.io/en/latest/module.html#localized-accents
# you can't change the voice gender
def text_to_speech_google(text, output_file, language_model):
    # Create a c object
    tts = gTTS(text=text, lang=language_model, slow=False)

    # Save the audio file
    tts.save(output_file)


# Mozilla tacotron2
# def text_to_speech_tacotron2(text, output_file):
#    audio = synthesize(text)
#    audio.save(output_file)
#    play_audio(output_file)


# import gdown


# mozilla_models = {
#     'en': {
#         'low': 'https://github.com/mozilla/TTS/releases/download/en/tts_models--en--ljspeech--tacotron2-DCA/model_file.pth.tar',
#         'high': 'https://github.com/mozilla/TTS/releases/download/en/tts_models--en--ljspeech--tacotron2-DCA/model_file.pth.tar'
#     },
#     'es': {
#         'low': 'https://github.com/mozilla/TTS/releases/download/en/tts_models--en--ljspeech--tacotron2-DCA/model_file.pth.tar',
#         'high': 'https://github.com/mozilla/TTS/releases/download/en/tts_models--en--ljspeech--tacotron2-DCA/model_file.pth.tar'
#     }
# }
#
#
# def download_model(language, level):
#     model_url = mozilla_models[language]
#     output_path = f"mozillamodels/{language}/{level}/model_file.pth.tar"
#     gdown.download(model_url, output_path, quiet=False)  # Set quiet=False to see download progress


def text_to_speech_mozilla(text, output_file, language_model):
    voice_synthesizer = synthesizer.Synthesizer()
    voice_synthesizer.vocoder_model("vocoder_models/universal/libri-tts/wavegrad")
    voice_synthesizer.tts(text='Hola, como estas?')
