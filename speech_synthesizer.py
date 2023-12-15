import pyttsx3
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager
from gtts import gTTS
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