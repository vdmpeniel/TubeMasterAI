# import time
#from TTS.tts.datasets import emotion
from numba import short

import media_processor
# import translator
# import media_downloader
#
import console_interface
import sys
import telemetry
import synthesizer_coqui as synthesizer
import file_manager
import re
import bible_reader as br
import tqdm
from collections import deque
#from TTS.api import TTS
import reader_service



def bible_reader(args):
    print('Starting Bible Reader')
    # br.read_full_bible_book('./workdirectory/KJV', 'kjv_bible.txt', 44)
    # br.read_bible_chapter_by_chapter('./workdirectory/KJV', 'kjv_bible.txt')

def say_hi(args):
    reader_service.read_out_loud(model=args[2], text='Hi there!', output_file_path='./workdirectory/123/hi.wav')

def get_speakers(args):
    console_interface.print_list('Speaker List', reader_service.get_speaker_list(args[2]))

def get_models(args):
    console_interface.print_list('Model List', reader_service.get_model_list())

def get_languages(args):
    console_interface.print_list('Language List', reader_service.get_language_list(args[2]))

def main():
    print('*** Welcome to TubeMasterAi Service ***')

    actions = {
        'bible-reader': bible_reader,
        'say-hi': say_hi,
        'get-models': get_models,
        'get-languages': get_languages,
        'get-speakers': get_speakers
    }
    tlmtry = telemetry.Telemetry()
    tlmtry.start()

    if len(sys.argv) > 1:
        actions[sys.argv[1]](sys.argv)
    else:
        raise Exception("No arguments provided")




    print(f'Telemetry: {tlmtry.stop()}')



    # simple_model_reader(model, text, output_file_path)
    # synthesizer.create_vctk_vits_model_voice_sampler(model=model, output_path='./workdirectory/123/')
    # processor = media_processor.MediaProcessor(
    #     '123',
    #     '001'
    # )
    #
    # processor.video_download_node({
    #     'url': 'https://www.youtube.com/shorts/X9lJojo9-cQ',
    #     'video_filename': 'video1.mkv',
    # })
    #
    # processor.extract_audio({
    #     'video_file_path': './workdirectory/123/001/video1.mkv',
    #     'output_audio_path': './workdirectory/123/speaker_output.wav'
    # })

    # processor.create_voice({
    #     'text': text,
    #     'generated_voice_path': './workdirectory/123/generated_voice.wav',
    #     'gtts_model': 'es'
    # })

    # synthesizer.text_to_speech_coqui_single_speaker(
    #     text,
    #     './workdirectory/123/output.wav',
    #     'en'
    # )

    # voice cloning with coqui
    # synthesizer.text_to_speech_coqui_cloning(
    #     text,
    #     './workdirectory/123/speaker_output.wav',
    #     './workdirectory/123/output.wav',
    #     'es'
    # )

    # synthesizer.text_to_speech_coqui_multiple_speaker(
    #     text=text,
    #     output_file='./workdirectory/123/output.wav',
    #     language_model='es',
    #     speaker_name='Claribel Dervla'
    # )

    # vtta_options = {
    #     'video_filename': 'video1.mkv',
    #     'source_language': 'en',
    #     'target_language': 'es',
    #     'level': 'low'
    # }
    # processor.video_to_translated_audio_node(vtta_options)

    # to be able to actually translate a text completely we need to introduce pauses and
    # split the text using those pause symbols

    # timer = telemetry.Telemetry()
    # transcription = {'text here'}
    # transcription = processor.correct_transcription(transcription, 'es', timer, 0)
    # print(transcription)
    #
    # translation = processor.translate(
    #     transcription,
    #     timer,
    #     100
    # )
    # print(translation)





if __name__ == '__main__':
    main()

    # remove_versions()


def find_operators(text):
    location = re.search(r'==|~=|>=|<=', text)
    return location


def remove_versions():
    reqs = file_manager.read('requirements.txt')
    req_list = reqs.split('\n')
    new_list = []
    for req in req_list:
        position = find_operators(req)
        position = len(req) if position is None else position.span()[0]
        new_list.append(req[0:position])

    data = '\n'.join(new_list)
    file_manager.save(data, 'requirements.txt', 'w')