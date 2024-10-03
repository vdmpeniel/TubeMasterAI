# import time
from TTS.tts.datasets import emotion

import media_processor
# import translator
# import media_downloader
#
import telemetry
import synthesizer_coqui as synthesizer
import file_manager
import re
from TTS.api import TTS


def simple_model_reader(model, text, output_file_path):
    speaker_list = synthesizer.get_model_speaker_list(model)
    print(f'Speaker Name List: {speaker_list}')

    language_list = synthesizer.get_model_language_list(model)
    print(f'Language List: {language_list}')

    synthesizer.text_to_speech_coqui_single_speaker(
        text=text,
        output_file=output_file_path,
        model=model
    )




def main(title):
    print(title)

    tmtry = telemetry.Telemetry()
    tmtry.start()
    model = 'tts_models/en/vctk/vits'
    text_file_path = './workdirectory/123/text.txt'
    output_file_path = './workdirectory/123/output.wav'
    text = file_manager.read(text_file_path)


    # simple_model_reader(model, text, output_file_path)
    synthesizer.vctk_vits_model_reader(
        text=text,
        model=model,
        speaker='p230',
        output_path=output_file_path,
        emotion='Happy',
        speed=0.8
    )
    # synthesizer.create_vctk_vits_model_voice_sampler(model=model, output_path='./workdirectory/123/')
    print(f'Telemetry: {tmtry.stop()}')

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


if __name__ == '__main__':
    main('Welcome to AudioMaster!')
    # remove_versions()
