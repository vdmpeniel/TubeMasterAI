# import time
#from TTS.tts.datasets import emotion
from matplotlib.pyplot import title

import media_processor
# import translator
# import media_downloader
#
import telemetry
import synthesizer_coqui as synthesizer
import file_manager
import re
import tqdm
from collections import deque
#from TTS.api import TTS


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


def verify_verses(bible_obj):
    print(f"Number of books: {len(bible_obj['books'])}")
    for book in bible_obj['books']:
        for verse in book['content']:
            print(f'{verse["reference"]} - {verse["text"]}')
            if not verse['text']:
                raise Exception(f'{book["name"]}-{verse["reference"]} is empty.')


def parse_bible_text(text):
    bible_obj = {}

    print('Adding title markings...')
    text = text.replace('\n\n\n', '<<<\n\n')

    print('Removing extra EOL characters...')
    text = text.replace('\n\n', '|').replace('\n', ' ')

    print('Splitting text lines...')
    lines = [line.strip() for line in text.split('|') if line not in ['', '\n']]

    print('Extracting source title...')
    bible_obj['source_title'] = lines.pop(0)
    print(f"Book Title: {bible_obj['source_title']}")
    # print(lines)
    # input("Press any key to continue...")

    # TODO: dividing the content in chapters
    print('Creating Bible Object...')
    bible_obj['books'] = []
    book_obj = {}
    content = []
    for i, line in tqdm.tqdm(enumerate(lines), total=len(lines)):
        # print(f'Processing line: {line}')
        matches = re.findall(r'(\d+:\d+)\s*(.*)', line)
        if ( # new chapter title is found
            not matches
            and ('<<<' in line)
            and (line[0].isupper())
            and (not re.search(r'[.,;:]', line[-4]))
        ):
            if len(book_obj) > 0:
                book_obj['content'] = content
                bible_obj['books'].append(book_obj)
                book_obj = {}
                content = []

            book_obj['name'] = line.replace('<<<', '')
            continue

        # actual text(verses or floating text)
        # floating verse (no verse reference)
        line = line.replace('<<<', '') # a few floating text lines were marked as titles
        if not matches and len(content) > 1:
            # print(f'Account for this --> {line}')
            content[-1]['text'] = content[-1]['text'] + ' ' + line
            continue

        # new verse/s by verse reference(chapter:verse)
        for match in matches:
            verse = {
                'reference': match[0],
                'text': match[1]
            }
            content.append(verse)

    bible_obj['books'].append(book_obj)
    book_obj['content'] = content


    # print(bible_obj)
    # verify_verses(bible_obj)


def read_the_bible(bible_source):
    tlmtry = telemetry.Telemetry()
    tlmtry.start()
    model = 'tts_models/en/vctk/vits'
    text_file_path = bible_source
    output_file_path = bible_source.removesuffix('.txt') + '.wav'
    text = file_manager.read(text_file_path)
    parse_bible_text(text)

    # synthesizer.vctk_vits_model_reader(
    #     text=text,
    #     model=model,
    #     speaker='p230',
    #     output_path=output_file_path,
    #     emotion='Happy',
    #     speed=0.1
    # )
    print(f'Telemetry: {tlmtry.stop()}')


def main(title):
    print(title)
    read_the_bible('./workdirectory/KJV/kjv_bible.txt')

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
