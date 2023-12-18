import json
import sys
import time
from typing import Union, Any

# import playsound
# from nltk.translate.ribes_score import corpus_ribes

import translator
from telemetry import Telemetry
import media_manager
from output_manager import OutputManager
import speech_recognition
import file_manager
import speech_synthesizer
import media_downloader
import utils


# noinspection PyTypeChecker
class MediaProcessor:

    def __init__(
            self,
            user_id,
            job_id
    ):
        self.logger = OutputManager()
        self.base_user_folder = f'workdirectory/{user_id}/'
        self.job_folder = self.base_user_folder + job_id + '/'

    def download_video(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Downloading Video...', options.progress)
        timer = Telemetry()
        timer.start()
        media_downloader.download_video_with_ytdlp(options.url, options.video_file_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)

    def extract_audio(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Extracting Audio...', options.progress)
        timer = Telemetry()
        timer.start()
        media_manager.extract_audio(options.video_file_path, options.output_audio_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)

    def convert_to_wav(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Converting to WAV...', options.progress)
        timer = Telemetry()
        timer.start()
        media_manager.convert_audio_to_wav(options.output_audio_path, options.wav_output_audio_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)

    def transcribe_audio(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Transcribing...', options.progress)
        timer = Telemetry()
        timer.start()
        transcription = speech_recognition.transcribe(options.wav_output_audio_path, options.vosk_model, options.transcription_level)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)
        return transcription

    def correct_text(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Correcting Transcription...', options.progress)
        timer = Telemetry()
        timer.start()
        corrected_transcription = speech_recognition.correct_text(options.text, options.language_code)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)
        return corrected_transcription

    def save(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Saving...', options.progress)
        timer = Telemetry()
        timer.start()
        file_manager.save_transcription(options.save_data, options.file_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)

    def translate_text(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Translating...', options.progress)
        timer = Telemetry()
        timer.start()
        translation = translator.do_translate(
            options.transcription_text,
            options.source_language,
            options.target_language
        )
        self.logger.log_message(f'Translation: {translation}', options.progress)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)
        return translation

    def create_voice(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        options = utils.DictToObj(options)
        self.logger.log_message('Creating Voice Audio...', options.progress)
        timer = Telemetry()
        timer.start()
        speech_synthesizer.text_to_speech_google(options.text, options.generated_voice_path, options.gtts_model)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', options.progress)

    def preprocess_video_to_translated_audio(self, options):
        output_audio_filename = file_manager.remove_extension(options.video_filename) + '_audio.mp3'
        wav_output_audio_filename = file_manager.remove_extension(output_audio_filename) + '.wav'
        generated_voice_filename = file_manager.remove_extension(options.video_filename) + '_generated_voice.wav'
        transcription_filename = file_manager.remove_extension(options.video_filename) + '_transcription.txt'
        translated_transcription_filename = file_manager.remove_extension(
            options.video_filename) + '_translated_transcription.txt'

        options.video_file_path = self.job_folder + options.video_filename
        options.output_audio_path = self.job_folder + output_audio_filename
        options.wav_output_audio_path = self.job_folder + wav_output_audio_filename
        options.generated_voice_path = self.job_folder + generated_voice_filename
        options.transcription_path = self.job_folder + transcription_filename
        options.translated_transcription_path = self.job_folder + translated_transcription_filename
        options.vosk_model = options.source_language
        options.gtts_model = options.target_language

    def video_download_node(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        timer = Telemetry()
        options = utils.DictToObj(options)
        options.video_file_path = self.job_folder + options.video_filename
        self.download_video(
            {
                'url': options.url,
                'video_file_path': options.video_file_path,
                'timer': timer,
                'progress': 100
            }  # type: dict[str, Union[int, Any]]
        )

    def video_to_translated_audio_node(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        timer = Telemetry()
        options = utils.DictToObj(options)
        self.preprocess_video_to_translated_audio(options)
        self.extract_audio(
            {
                'video_file_path': options.video_file_path,
                'output_audio_path': options.output_audio_path,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
        self.convert_to_wav(
            {
                'output_audio_path': options.output_audio_path,
                'wav_output_audio_path': options.wav_output_audio_path,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
        options.transcription = self.transcribe_audio(
            {
                'wav_output_audio_path': options.wav_output_audio_path,
                'vosk_model': options.vosk_model,
                'transcription_level': options.level,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
        options.transcription['text'] = self.correct_text(
            {
                'text': options.transcription['text'],
                'language_code': options.source_language,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
        self.save(
            {
                'save_data': options.transcription,
                'file_path': options.translated_transcription_path,
                'timer': timer,
                'progress': 75
            }  # type: dict[str, Union[int, Any]]
        )
        options.translated_transcription = json.loads(json.dumps(options.transcription))  # make a copy
        options.translated_transcription['text'] = self.translate_text(
            {
                'transcription_text': options.transcription['text'],
                'source_language': options.source_language,
                'target_language': options.target_language,
                'timer': timer,
                'progress': 75
            }  # type: dict[str, Union[int, Any]]
        )
        options.translated_transcription['text'] = self.correct_text(
            {
                'text': options.translated_transcription['text'],
                'language_code': options.target_language,
                'timer': timer,
                'progress': 75
            }  # type: dict[str, Union[int, Any]]
        )
        self.save(
            {
                'save_data': options.translated_transcription,
                'file_path': options.transcription_path,
                'timer': timer,
                'progress': 85
            }  # type: dict[str, Union[int, Any]]
        )
        self.create_voice(
            {
                'text': options.translated_transcription.text,
                'generated_voice_path': options.generated_voice_path,
                'timer': timer,
                'progress': 100
            }  # type: dict[str, Union[int, Any]]
        )

        # play generated audio - Comment this in production
        media_manager.play_audio(options.generated_voice_path)

    def video_transcription_node(self, options=None):
        if not options:
            raise ValueError('Options object is empty.')

        timer = Telemetry()
        self.convert_to_wav(
            {
                'output_audio_path': options.output_audio_path,
                'wav_output_audio_path': options.wav_output_audio_path,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
        options.transcription = self.transcribe_audio(
            {
                'wav_output_audio_path': options.wav_output_audio_path,
                'vosk_model': options.vosk_model,
                'transcription_level': options.level,
                'timer': timer,
                'progress': 70
            }  # type: dict[str, Union[int, Any]]
        )
