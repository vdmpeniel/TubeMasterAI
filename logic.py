import json
import sys
import time
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


class FullVideoProcessor:

    def __init__(
            self,
            user_id,
            job_id,
            url,
            video_filename,
            translation_source_language='en',
            translation_target_language='es',
            transcription_level='low'
    ):
        self.logger = OutputManager()
        self.base_user_folder = f'workdirectory/{user_id}/'
        self.job_folder = self.base_user_folder + job_id + '/'

        output_audio_filename = file_manager.remove_extension(video_filename) + '_audio.mp3'
        wav_output_audio_filename = file_manager.remove_extension(output_audio_filename) + '.wav'
        generated_voice_filename = file_manager.remove_extension(video_filename) + '_generated_voice.wav'
        transcription_filename = file_manager.remove_extension(video_filename) + '_transcription.txt'
        translated_transcription_filename = file_manager.remove_extension(
            video_filename) + '_translated_transcription.txt'

        self.url = url
        self.video_file_path = self.job_folder + video_filename
        self.output_audio_path = self.job_folder + output_audio_filename
        self.wav_output_audio_path = self.job_folder + wav_output_audio_filename
        self.generated_voice_path = self.job_folder + generated_voice_filename

        self.transcription_level = transcription_level
        self.transcription_path = self.job_folder + transcription_filename
        self.translated_transcription_path = self.job_folder + translated_transcription_filename
        self.translation_source_language = translation_source_language
        self.translation_target_language = translation_target_language
        self.vosk_model = translation_source_language
        self.gtts_model = translation_target_language

    def download_video(self, timer, progress):
        self.logger.log_message('Downloading Video...', progress)
        timer.start()
        media_downloader.download_video_with_ytdlp(self.url, self.video_file_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)

    def extract_audio(self, timer, progress):
        self.logger.log_message('Extracting Audio...', progress)
        timer.start()
        media_manager.extract_audio(self.video_file_path, self.output_audio_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)

    def convert_to_wav(self, timer, progress):
        self.logger.log_message('\nConverting to WAV...', progress)
        timer.start()
        media_manager.convert_audio_to_wav(self.output_audio_path, self.wav_output_audio_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)

    def transcribe_audio(self, timer, progress):
        self.logger.log_message('\nTranscribing...', progress)
        timer.start()
        transcription = speech_recognition.transcribe(self.wav_output_audio_path, self.vosk_model,
                                                      self.transcription_level)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)
        return transcription

    def correct_transcription(self, transcription, language_code, timer, progress):
        self.logger.log_message('\nCorrecting Transcription...', progress)
        timer.start()
        corrected_transcription = speech_recognition.correct_text(transcription, language_code)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)
        return corrected_transcription

    def save(self, data, file_path, timer, progress):
        self.logger.log_message('\nSaving...', progress)
        timer.start()
        file_manager.save_transcription(data, file_path)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)

    def translate(self, transcription, timer, progress):
        self.logger.log_message('\nTranslating...', progress)
        timer.start()
        translated_transcription = json.loads(json.dumps(transcription))  # make a copy
        translated_transcription['text'] = translator.do_translate(
            translated_transcription['text'],
            self.translation_source_language,
            self.translation_target_language
        )
        self.logger.log_message(f'Translation: {translated_transcription["text"]}', progress)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)
        return translated_transcription

    def create_voice(self, translated_transcription, timer, progress):
        # Create voice audio
        self.logger.log_message('\nCreating Voice Audio...', progress)
        timer.start()
        speech_synthesizer.text_to_speech_google(translated_transcription["text"], self.generated_voice_path, self.gtts_model)
        self.logger.log_message(f'Execution Time: {timer.stop()} seconds', progress)

    def run_video_to_translated_audio(self):
        timer = Telemetry()
        self.download_video(timer, 0)
        self.extract_audio(timer, 10)
        self.convert_to_wav(timer, 30)
        transcription = self.transcribe_audio(timer, 65)
        transcription = self.correct_transcription(transcription, self.translation_source_language, timer, 70)
        self.save(transcription, self.transcription_path, timer, 75)
        translated_transcription = self.translate(transcription, timer, 80)
        translated_transcription = self.correct_transcription(translated_transcription, self.translation_target_language, timer, 83)
        self.save(translated_transcription, self.translated_transcription_path, timer, 85)
        self.create_voice(translated_transcription, timer, 100)

    def run_video_transcription_node(self):
        timer = Telemetry()
        self.download_video(timer, 0)
        self.extract_audio(timer, 10)
        self.convert_to_wav(timer, 30)
        transcription = self.transcribe_audio(timer, 65)
        transcription = self.correct_transcription(transcription, self.translation_source_language, timer, 70)
        self.save(transcription, self.transcription_path, timer, 75)

    # API
    def video_to_translated_audio(self):
        timer = Telemetry()
        timer.start()
        self.logger.log_message(f'Starting VideoToTranslatedAudio Node...: {timer.stop()}', 100)
        self.run_video_to_translated_audio()
        self.logger.log_message(f'Total Execution Time: {timer.stop()}', 100)

        # play generated audio - Comment this in production
        media_manager.play_audio(self.generated_voice_path)

    def video_transcription_node(self):
        timer = Telemetry()
        timer.start()
        self.logger.log_message(f'Starting VideoTranscription Node...: {timer.stop()}', 0)
        self.run_video_transcription_node()
        self.logger.log_message(f'Total Execution Time: {timer.stop()}', 100)
