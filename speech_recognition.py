import sys
import wave
import json
import speech_recognition as sr
import vosk
from vosk import Model, KaldiRecognizer, SetLogLevel
from google.cloud import speech_v1p1beta1 as speech
import language_tool_python
from language_tool_python import LanguageTool
import spacy


def download_spacy_model(model_name):
    # Check if the model is already installed
    if model_name not in spacy.util.get_installed_models():
        # If not installed, download the model
        spacy.cli.download(model_name)


def transcribe_audio_google_cloud(api_key, audio_path):
    client = speech.SpeechClient()
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": "en-US",  # Adjust the language code as needed
        "audio_channel_count": 2,
    }

    response = client.recognize(config=config, audio=audio)

    print('Generated text:')
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))


def transcribe_audio_pocketsphinx(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_sphinx(audio)
        # text = recognizer.recognize_sphinx(audio, language_model_path=language_model, dictionary_path=dictionary)
        return text

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")


def transcribe_audio_vosk(vosk_model, audio_path):
    SetLogLevel(0)
    sample_rate = 16000

    # Initialize Vosk recognizer
    model = Model(lang=vosk_model)
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)

    # Read audio file
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Perform recognition
    recognizer.AcceptWaveform(audio_data)
    result = recognizer.Result()

    return json.loads(result)


def transcribe_audio_vosk_chunks(model, audio_path, chunks=1):
    # You can set log level to -1 to disable debug messages
    SetLogLevel(-1)

    waveform = wave.open(audio_path, "rb")
    if waveform.getnchannels() != 1 or waveform.getsampwidth() != 2 or waveform.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    model = Model(lang=model)
    frame_rate = waveform.getframerate()

    recognizer = KaldiRecognizer(model, frame_rate)
    recognizer.SetWords(True)
    recognizer.SetPartialWords(True)

    result_list = []
    while True:
        data = waveform.readframes(int(waveform.getnframes() / chunks))
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result_list.append(recognizer.Result())
        else:
            result_list.append(recognizer.PartialResult())

        # result_list.append(recognizer.FinalResult())
    return result_list


vosk_model_dict = {
    'en': {'big': 'vosk-model-en-us-0.21', 'small': 'vosk-model-small-en-us-0.15'},
    'fr': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-es-0.42'},
    'de': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'es': {'big': 'vosk-model-es-0.42', 'small': 'vosk-model-small-es-0.42'},
    'it': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'ru': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'pt': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'ja': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'ko': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
    'zh': {'big': 'vosk-model-fr-0.22', 'small': 'vosk-model-small-en-us-0.15'},
}


def transcribe_audio_vosk_complex(vosk_model, audio_path, hd=False):
    # You can set log level to -1 to disable debug messages
    SetLogLevel(-1)

    waveform = wave.open(audio_path, "rb")
    if waveform.getnchannels() != 1 or waveform.getsampwidth() != 2 or waveform.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    # Download model if doesn't exist
    model = Model(lang=vosk_model)
    if hd:
        print(f"Model's Path: {model.get_model_by_name(model_name=vosk_model_dict[vosk_model]['big'])}")
    else:
        print(f"Model's Path: {model.get_model_by_name(model_name=vosk_model_dict[vosk_model]['small'])}")
        # print(f"Model's Path: {model.get_model_by_lang(lang=vosk_model)}")  # Download model if doesn't exist

    frame_rate = waveform.getframerate()

    recognizer = KaldiRecognizer(model, frame_rate)
    recognizer.SetWords(True)
    recognizer.SetPartialWords(True)

    data = waveform.readframes(int(waveform.getnframes()))
    if len(data) == 0:
        raise Exception('No audio data found.')
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
    else:
        raise Exception('Error accepting audio data.')
    return json.loads(result)


def correct_capitalization_lt(text):
    with LanguageTool('en_Us') as tool:
        # Get suggestions for the entire text
        matches = tool.check(text)

        for match in matches:
            print(match.ruleId)

        # Filter suggestions for capitalization issues
        capitalization_matches = [match for match in matches if match.ruleId.endswith('LOWERCASE')]

        # Apply corrections for capitalization
        corrected_text = language_tool_python.utils.correct(text, capitalization_matches)
        return corrected_text


def full_text_correction_lt(text, language_model):
    language_model = 'en_Us' if language_model == 'en' else language_model

    with LanguageTool(language_model) as tool:
        # Get suggestions for the entire text
        matches = tool.check(text)

        # Apply corrections for capitalization
        corrected_text = tool.correct(text)

        return corrected_text


# Get models here: https://spacy.io/models
iso_language_to_spacy_model_dict = {
    'en': {
        'efficiency': 'en_core_web_sm',
        'accuracy': 'en_core_web_trf',
    },
    'es': {
        'efficiency': 'es_core_news_sm',
        'accuracy': 'es_dep_news_trf',
    }
}


def add_punctuation_spacy(text, language_code='en', mode='efficiency'):
    model = iso_language_to_spacy_model_dict[language_code][mode]
    download_spacy_model(model)
    nlp = spacy.load(model)

    # Process the text using spaCy
    doc = nlp(text)

    # Reconstruct sentences with added punctuation
    corrected_text = ' '.join([sentence.text.strip() + '.' for sentence in doc.sents])
    return corrected_text


def correct_text(text, language_code):
    text = add_punctuation_spacy(text, language_code, 'efficiency')
    text = full_text_correction_lt(text, language_code)
    return text


# def add_punctuation(transcription):
#     transcription_dict = json.loads(transcription[0])
#     text = transcription_dict['text']
#     tokens = nltk.word_tokenize(text)
#     text_with_punctuation = nltk.pos_tag(tokens)
#     transcription_dict['text'] = text_with_punctuation
#     transcription[0] = json.dumps(transcription_dict, indent=2)


def transcribe(wav_output_audio_path, vosk_model, transcription_level='low'):
    # transcribe_audio_google_cloud("downloads_{user_id}/audio1.mp3")
    # transcribe_audio_pocketsphinx(wav_output_audio_path)
    # transcription = transcribe_audio_vosk(vosk_model, wav_output_audio_path)
    transcription = transcribe_audio_vosk_complex(vosk_model, wav_output_audio_path, transcription_level == 'high')
    return transcription
